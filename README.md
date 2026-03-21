# NeuralChat - Local AI Chatbot

A privacy-focused AI chatbot that runs entirely on your machine using Ollama. No internet connection needed, no API keys, no data ever leaves your device.

Built with Streamlit for the UI and Ollama for running open-source LLMs locally.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-green)

## What it does

- Chat with AI models running locally on your machine
- Switch between models like TinyLlama, Llama 3.2, Gemma, Mistral
- Adjust creativity (temperature) to get factual or creative responses
- All conversations stay on your device, nothing goes to the cloud

## Tech Stack

| Technology | Why I used it |
|------------|---------------|
| Python | main language, most comfortable with it |
| Streamlit | fastest way to build a web UI without writing HTML/JS |
| Ollama | lets you run LLMs locally without GPU or cloud setup |
| Llama 3.2 / TinyLlama | open source models by Meta, free to use |
| Requests | to make HTTP calls to Ollama's local API |

## How it works

1. Ollama runs in the background and serves AI models on `localhost:11434`
2. User types a message in the Streamlit chat UI
3. The app sends the message to Ollama's API using requests library
4. Ollama processes it through whichever model is selected
5. Response comes back and gets displayed in the chat

Everything runs locally. No cloud, no API keys.

## Setup

### You need
- Python 3.10+
- Ollama installed ([download here](https://ollama.com))

### Steps

1. Install Ollama and pull a model
   ```bash
   # after installing ollama
   ollama pull tinyllama       # small model, works on low RAM
   ollama pull llama3.2        # bigger model, needs 4GB+ RAM
   ```

2. Clone the repo
   ```bash
   git clone https://github.com/yourusername/ollama-app.git
   cd ollama-app
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure Ollama is running
   ```bash
   ollama serve
   ```

5. Start the app
   ```bash
   streamlit run ollama_app.py
   ```

6. Open `http://localhost:8501` in your browser

## Project Structure

```
ollama-app/
  ollama_app.py       # main file - UI + chat logic + API calls
  requirements.txt    # python packages needed
  .gitignore          # files to ignore in git
  README.md           # this file
```

## What I learned

- How to work with local LLMs using Ollama
- Building interactive UIs with Streamlit
- Making API calls to local services
- Managing chat state/session in Streamlit
- CSS styling within Streamlit using markdown injection

## Future scope

- Add document upload (PDF/text) so users can ask questions about their files
- Stream responses word-by-word instead of waiting for the full answer
- Add conversation memory so the AI remembers previous messages
- Export chat history as a text file
