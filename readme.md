# LLM-Chat Application using Ollama and Streamlit

Using Ollama, running LLMs locally becomes very easy. Ollama offers many Open-Source LLMs, which can be downloaded.
Because Ollama itself only offers a Server + Client or Terminal Interface, I wanted to create a simple chat GUI using Streamlit.
I also want to integrate an option to let the LLM "talk" using OpenAI's TTS-model. For this, an OpenAI API-Key is necessary and needs to be included in the .env file.

Using ChromaDB, ist possible to implement simple RAG-capabilites. I implemented embeddings for Markdown files to use with my Obsidian Knowledge Base. You need to provide a path to a directory which includes .md files in your .env file, as well as pulling the embedding model all-minilm from ollama. You can also use another embedding-model, just change the code accordingly.

Right now, the application is using LLama3-8b model. In the future, I will implement a selection of models. I did not make any changes to the LLama model.

Ollama uses MIT License.

**Ollama_tts.py is a terminal-only application, no streamlit included.**

**st_app.py includes a Web-GUI using Streamlit**

### Sources

Streamlit: https://streamlit.io

Ollama: https://ollama.com

OpenAI API: https://platform.openai.com/docs/overview
