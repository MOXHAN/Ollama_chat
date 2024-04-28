# LLM-Chat Application using Ollama

Using Ollama, running LLMs locally becomes very easy. Ollama offers many Open-Source LLMs, which can be downloaded.
Because Ollama itself only offers a Server + Client or Terminal Interface, I wanted to create a simple chat GUI using Streamlit.
I also want to integrate an option to let the LLM "talk" using OpenAI's TTS-model. For this, an OpenAI API-Key is necessary and needs to be included in the .env file.

Right now, the application is using LLama3-8b model. In the future, I will implement a selection of models. I did not make any changes to the LLama model.

Ollama uses MIT License.

**Ollama_tts.py is a terminal-only application, no streamlit included.**

**st_app.py includes a Web-GUI using Streamlit**

### Sources

Streamlit: https://streamlit.io

Ollama: https://ollama.com

OpenAI API: https://platform.openai.com/docs/overview