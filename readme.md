# **Introduction**

This project aims to leverage existing personal notes of various topics using Large Language Models (LLMs). The notes are available in markdown format and therefore easily readable for both machines and humans in raw format. However, the main usage in this projects scenario is through the note-taking app Obsidian (LINK HERE).

## **Obsidian and Open-Source**

Obsidian shines through its transparancy in comparison to other apps like Notion. By using the markdown format, taken notes are independent of the Obsidian app and can be just as well read in a simple editor. To support this ideology, which fits very well into the Open-Source idea, I aim to use (Open-Source) non-proprietary LLMS, like Llama, to "chat" with my notes. This will allow me better access to ther knowledge I have saved in my notes and furthermore expand it by the knowledge of the LLM, if necessary.

## **RAG Workflow**

Obsidian saves all markdown files in one folder, which of course can have a more complex sub-structure. This folder is called the "vault". To give a LLM access to my vault, I will create contexttual embeddings of the note files. Contextual embeddings are created using an embedding model and do not only convert single words into a numerical representation (vectors), but also capture the context they appear in. The vectors then will be stored in a persistent database, which allows the LLM acces to it. Everytime I will send a Prompt to the LLM, it will compare the prompts context to all my notes and retrieve useful information for the answer, if available.

## **Challenges**

### 1. The perfect prompt

A major challenge is the prompt engineering, which describes writing the best prompt to get the best possible answer. To do that I first create a list of requirements for the LLMS answer:
1. I only want it to use my notes, if it actually fits the question and is useful and otherwise fall back to its own general knowledge
2. I want the LLM to tell me what source it used (my notes or its own knowledge)

### 2. Evaluation

To evaluate a LLM is a difficult task, as there are no simple metrics like accuracy. Thus I will evaluate the entire RAG-workflow, so the LLM + embedding model, especially for my use case, meaning how useful is it really. To do this in the best possible way, I came up with the following questions I will evaluate the workflow on:

1. To what extend of completeness has the actually matching content available in the notes been used in the response?
2. How good/effective has the available content been used for the response?
3. Were all points mentioned in the prompt attended?
4. Extend of Hallucination and/or using wrong/not aimed for information (10 = much hallucination)

Each question will be evaluated on a scale from 0 to 10, where 0 is the worst and 10 the best possible outcome.

## **LLMs and Embedding-Models Choice**

I tested the following LLMs:

1. **Llama 3 8B**
2. **Llama 3.2 1B**
3. **gemma2 2B**
4. **phi 3.5 3.8B**

And I will use the embedding model **nomic-embed-text**.

## **The Application**

The actual application presenting a chat-interface to communicate with the LLM is a Streamlit GUI. A Dockerfile ready to build is included in this repo. Simply use the command docker build and start the container.