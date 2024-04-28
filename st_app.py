import streamlit as st
import ollama
from typing import Dict, Generator
import threading
import queue
import pyaudio
from openai import OpenAI
from dotenv import load_dotenv
import os

#################### Audio Player Class ####################

class AudioPlayer(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.queue = queue.Queue()
        self.daemon = True
        self.start()

    def run(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self.play_audio(text)
            self.queue.task_done()

    def play_audio(self, text):
        player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            response_format="pcm",
            speed=1.0,
            input=text,
        ) as response:
            for chunk in response.iter_bytes(chunk_size=1024):
                player_stream.write(chunk)

        player_stream.close()

    def add_to_queue(self, text):
        self.queue.put(text)

#################### Ollama Generator Function using TTS ####################

def ollama_generator_tts(audio_player, messages: Dict) -> Generator:
    stream = ollama.chat(
        model="llama3", messages=messages, stream=True)
    buffer_txt = ""  # Buffer to store text before sending to TTS
    for chunk in stream:
        # Buffer the message content
        buffer_txt += chunk['message']['content']
        # Check for full stops or other suitable points to split the text
        if buffer_txt and (buffer_txt.endswith(('.', '!', '?')) or chunk.get("done", False)):
            # Add buffered text to TTS queue
            audio_player.add_to_queue(buffer_txt)
            # Reset buffer after sending to TTS
            buffer_txt = ""

        yield chunk['message']['content']

#################### Ollama Generator Function ####################

def ollama_generator( messages: Dict) -> Generator:
    stream = ollama.chat(
        model="llama3", messages=messages, stream=True)
    
    for chunk in stream:
        yield chunk['message']['content']

#################### Streamlit code ####################

st.title("Llocal LLama")

if "tts" not in st.session_state:
    st.session_state.tts = False

# Toggle TTS mode depending on button press
with st.sidebar:
    if st.button("Toggle TTS"):
        st.session_state.tts = not st.session_state.tts

    # Add field to enter API key
    api_key = st.text_input("OpenAI API Key", type="password")
    if "api_key" not in st.session_state:
        load_dotenv()
        # set api key depending on whether it is provided in the .env file or the field
        if not os.getenv("OPENAI_API_KEY"):
            st.session_state.api_key = api_key
        else:
            st.session_state.api_key = os.getenv("OPENAI_API_KEY")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.tts:
    # Initialize OpenAI client
    if "client" not in st.session_state:
        try:
            st.session_state.client = OpenAI(api_key=st.session_state.api_key)
        except Exception as e:
            with st.chat_message("assistant"):
                st.write(f"Error: {e}\n You did not provide a valid OpenAI API key. Please provide a valid API key in the .env file or field on the sidebar.")
    
    # initialize audio player
    if "audio_player" not in st.session_state:
        st.session_state.audio_player = AudioPlayer(client=st.session_state.client)

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
        if st.session_state.tts:
            response = st.write_stream(ollama_generator_tts(st.session_state.audio_player, st.session_state.messages))
        else:
            response = st.write_stream(ollama_generator(st.session_state.messages))
        
        st.session_state.messages.append({"role": "assistant", "content": response})