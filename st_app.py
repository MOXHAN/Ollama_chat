import streamlit as st
import ollama
from typing import Dict, Generator
import threading
import queue
import pyaudio
from openai import OpenAI
from dotenv import load_dotenv
import os
from embeddings import createMarkdownEmbeddings, initChroma

#################### Ollama Generator Function ####################

def ollama_generator( messages: Dict, collection) -> Generator:

    # get current prompt
    currentPrompt = messages[-1]["content"]

    # generate an embedding for the prompt
    response = ollama.embeddings(
        prompt=currentPrompt,
        model="nomic-embed-text"
    )
    # retrieve the most relevant doc
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=1
    )
    # get the data from results
    try:
        data = results['documents'][0][0]

        # add the retrieved doc-information to the prompt
        modifiedPrompt = f"""Notes: {data}
        Answer the following question based on the provided notes, if relevant and available,
        otherwise use your own knowledge to provide an accurate response.
        After answering, indicate the source by specifying either 'from notes' or 'from general knowledge'. Here is the question: {currentPrompt}"""
        
        # write modified prompt back to the messages dict
        messages[-1]["content"] = modifiedPrompt

    except:
        print("No relevant data found")
    
    stream = ollama.chat(
        model=st.session_state.llm, messages=messages, stream=True)
    
    for chunk in stream:
        yield chunk['message']['content']

#################### Streamlit code ####################

def streamlit_app():
    
    st.title("Llocal LLama")

    # Init used LLM
    if "model" not in st.session_state:
        st.session_state.llm = "llama3"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add sidebar menu to choose LLM model
    with st.sidebar:
        llm = st.selectbox("Select Model", ["llama3", "llama3.2:1b", "gemma2:2b","phi3.5"])
        st.session_state.llm = llm

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            
            response = st.write_stream(ollama_generator(st.session_state.messages, st.session_state["collection"]))
            
            st.session_state.messages.append({"role": "assistant", "content": response})


def main():

    # only create embeddings once
    if "collection" not in st.session_state:
        # create embeddings for all markdown files in the directory
        collection = createMarkdownEmbeddings()
        st.session_state.collection = collection
    

    # start the streamlit app
    streamlit_app()


if __name__ == "__main__":

    main()