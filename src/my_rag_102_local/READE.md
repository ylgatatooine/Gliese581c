# My RAG 102

A simple Retrieval-Augmented Generation (RAG) system running locally.

## Features

- **LLM & Embedding:** Uses [Ollama](https://ollama.com/) with Llama 3.2 for both language modeling and embedding.
- **Vector Database:** Utilizes [Chroma DB](https://www.trychroma.com/) for efficient vector storage and retrieval.
- **Local Execution:** No cloud dependencies; all components run on your machine.

## Getting Started

1. **Install Ollama** and download the Llama 3.2 model.
2. **Pull embedding model** locally.
```
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF

# Remember to install 
pip install ollama
```

3. **Run the application** following the instructions in your project.


## Usage

- Add your documents to the system.
- Query using natural language; relevant context is retrieved and passed to the LLM for response generation.

## Requirements

- Python 3.8+
- Ollama
- Chroma DB

## License

MIT
