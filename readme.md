# **Installation and Setup**

**Requirements:**

1. Docker
2. Ollama

**Ollama**

To run the LLM models locally, I used Ollama in this project. Both windows and macOS apps are available, running Ollama in WSL or Docker also works. After installing Ollama, the models are served by default under the port 11434. This is what the API in this project expects. If you are already using this port or for example the port from the Ollama Docker Container isnt exposed, you need to make changes accordingly. That said, the most simple way is using the downloadable apps. Ollama: https://ollama.com/download

To use any model, you first need to download it. If you install Ollama through the app or in WSL you can use the CLI (command-line interface) of ollama and pull the models like so:

````
ollama pull gemma2:2b
````

After that, the models are ready to go. You can also test the models in the CLI by running the following command:

````
ollama run gemma2:2b
````

And finally, you can check the correct setup and availability of the API under the correct port by going to localhost:11434 in your browser. It should say "Ollam is running".

**Project setup**

1. Clone the repo
2. Create an .env file and write "DIRECTORY=path/to/your/obsidian/vault", to test with the provided notes it would be "DIRECTORY=notes"
3. Either directly run the command "streamlit run st_app.py" to run the code from within your file-system
4. Or build the docker image "docker build -t ollama_chat ."  and run the container "docker run ollama_chat"
5. Go to localhost:8501 where the streamlit-GUI can be found
6. Choose an installed model in the sidebar and start chatting!

# **Project Introduction**

This project aims to leverage existing personal notes of various topics using Large Language Models (LLMs). The notes are available in markdown format and therefore easily readable for both machines and humans in raw format. However, the main usage in this projects scenario is through the note-taking app Obsidian (LINK HERE).

## **Obsidian and Open-Source**

Obsidian shines through its transparancy in comparison to other apps like Notion. By using the markdown format, taken notes are independent of the Obsidian app and can be just as well read in a simple editor. To support this ideology, which fits very well into the Open-Source idea, I aim to use (Open-Source) non-proprietary LLMS, like Llama, to "chat" with my notes. This will allow me better access to ther knowledge I have saved in my notes and furthermore expand it by the knowledge of the LLM, if necessary.

## **RAG Workflow**

Obsidian saves all markdown files in one folder, which of course can have a more complex sub-structure. This folder is called the "vault". To give a LLM access to my vault, I will create contexttual embeddings of the note files. Contextual embeddings are created using an embedding model and do not only convert single words into a numerical representation (vectors), but also capture the context they appear in. The vectors then will be stored in a persistent database, which allows the LLM acces to it. Everytime I will send a Prompt to the LLM, it will compare the prompts context to all my notes and retrieve useful information for the answer, if available.

---

## **Challenges**

### 1. The perfect prompt

A major challenge is the prompt engineering, which describes writing the best prompt to get the best possible answer. To do that I first create a list of requirements for the LLMS answer:
1. I only want it to use my notes, if it actually fits the question and is useful and otherwise fall back to its own general knowledge
2. I want the LLM to tell me what source it used (my notes or its own knowledge)

To find a prompt that leads the LLM to answer both points, I used ChatGPT 4o as help and came up with the following prompt: "Answer the following question based on the provided notes, if relevant and available, otherwise use your own knowledge to provide an accurate response. After answering, indicate the source by specifying either 'from notes' or 'from general knowledge'. Here’s the question:"

### 2. Evaluation

To evaluate a LLM is a difficult task, as there are no simple metrics like accuracy. Thus I will evaluate the entire RAG-workflow, so the LLM + embedding model, especially for my use case, meaning how useful is it really. To do this in the best possible way, I came up with the following questions I will evaluate the workflow on:

1. To what extend of completeness has the actually matching content available in the notes been used in the response?
2. How good/effective has the available content been used for the response?
3. Were all points mentioned in the prompt attended?
4. Extend of Hallucination and/or using wrong/not aimed for information (For the purpose of calculating a total score at the end, this score is in the range of -10 to 0 with -10 = much hallucination, 0 = no hallucination)

Each question will be evaluated on a scale from 0 to 10, where 0 is the worst and 10 the best possible outcome.

## **LLMs and Embedding-Models Choice**

I tested the following LLMs:

1. **Llama 3 8B**
2. **Llama 3.2 1B**
3. **gemma2 2B**
4. **phi 3.5 3.8B**

And I will use the embedding model **nomic-embed-text**.

---

## **The Application**

The actual application presenting a chat-interface to communicate with the LLM is a Streamlit GUI. A Dockerfile ready to build is included in this repo. Simply use the command docker build and start the container.

---

# **Testing**

In this repo are 3 different note files in markdown format, which are copies from my original vault. I will ask every model 3 questions about each note and evaluate it on the questions I listed before. The results can be found in the results.xlsx and are presented below. Each answer is zero-shot, meaning I ask each question only once and evaluate the answer.

For each note, I will simply ask the model what it can tell me about the topic mentioned in the title of the note, based on my notes. For example, if the note is called "RAG Workflows", I will ask the model to tell me about RAG workflows, based on my notes. The second and third question will be a follow-up, which is topic-specific. The questions and answers are included in the results file.

**REMARK**

The rest of my notes are not included in this repo. Sometimes "wrong" notes or not the notes I intended the LLM to use were retrieved by the RAG-workflow, which therefore lead to mistakes that arent reproducible with this repo.

---

# **Results**

In this Readme I will simply present the overall leaderboard. A more in depth look at the results for each topic can be found in the notebook "portfolio.ipynb".

## **I. Leaderboard**

1. Gemma2 2B - 277 Points
2. Llama3 8B - 233 Points
3. Phi3.5 3.8B - 145 Points
4. Llama3.2 1B - 101 Points

---

## **II. Observations**

The following observations are **heavily biased** and were written based on my (the testers) experience and opinion when using the models.

**Llama3**
- stays close to provided content
- always provides source in the same manner

**Llama3.2 1B**
- "strays" from provided content --> it mixes provided and own knowledge, not clearly marking when it does it. While this can be useful, its not clear how much the provided knowledge is used at all
- very often uses noticebly own knowledge and still states it as "Source: your notes"
- sometimes mixes up topics or uses completely irrelevant information

**Gemma2 2B**
- uses emojis --> positive experience
- general tone and "way of talking" sounds better than Llama3.2 1B and Llama3
	- Uses rhetorical methods: (What are they? Pandas DataFrames are essentially tables of data. Think of them like spreadsheets or databases with rows and columns that organize your information neatly. Why are they useful? They provide a powerful way to store and manipulate structured data in Python, making it much easier than handling raw arrays.)
- often uses provided notes and adds own knowledge to further explain
	- but also keeps answers short if question is clear and only requires short, precise answer
	- anyway always states the source would be from notes

**Phi 3.5**
- hallucinates non-existent words sometimes (e.g.: Don´thy)
- often uses provided notes and adds own knowledge to further explain, but anyway states the source would be from notes
- in comparison to gemma2, writes lengthy answers
- has a "weird" style, uses brackets a lot, mentions source in an unclear way ("all indicators point back here")
- understands Obsidian "tags" (mentioned it and understood its context)
- sometimes mentions exact note used as source, which is good
- sometimes only produces hallucination: invents words, writes japanese or other non-latin letters and complete "nonsense", meaning sentences with no meaning or structure.

---

## **III. Conclusion / Personal Opinion**

First of all, it is important to mention that the RAG-Workflow "failed" multiple times, as shown above and provided unmatching content to the LLMs, although the embedding model and the content or the questions werent changed throughout the testing. Therefore the testing environment wasnt always the same to a hundred percent, even if no changes to the code or system were made. However, I inted this project to be useful for the end-user (myself) and therefore want to evaluate the experience the user has when using the system. "Pressing out" the last possible points a model can reach is not serving the purpose of this project, but evaluating first-try experience is.

The prompt used is another crucial part of the RAG-workflow, along with the correct retrieval of embeddings. As explained in the Introduction, I wanted the LLM to fulfill two major guidelines: first, to stick to my notes and only fall back to its own knowledge if necessary and second, to always provide a source. While all models fulfilled the second task in every response, it was often untrue. As listed in the observations, some models, like Gemma2, often mixed the knowledge from my notes and their own knowledge, but still stated the source to be my notes. This is rather unsatisfying. Furthermore, a clear line between own and provided knowledge cant be drawn. Therefore the models cant be evaluated in a comprehensive way for this matter. This is also the case for the first guideline. It is difficult to determine, wether it was necessary or not, in cases where the model mixed-in its own knowledge. For the prompt, I can simply conclude that all models always provide a source, wether it is true or not and the first guideline is very "flexible", making an evaluation very difficult. Further prompt-engineering could lead to the models sticking closer to the rules, but also effect the user-experience.

To sum it up, based on the provided scoring and the observations, **my personal favorite and the overall best experience I had with Gemma2 2B.**

---

# **Final Remark**

It is important to keep in mind that the tested models have different amounts of parameters and use different amounts of memory, because they were made for different purposes. A Llama3 with 8B will always overall perform better than a Llama3.2 with only 1B. Therefore, the hardware one intends to use the LLM on has to be taken into consideration when using the testing and scoring as means to evaluate which model to use.

---

# **Sources**

Obsidian: https://obsidian.md

Streamlit: https://streamlit.io

Ollama: https://ollama.com