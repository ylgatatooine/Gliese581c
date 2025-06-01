# Personal RAG from Scratch

This project demonstrates how to build a simple Retrieval-Augmented Generation (RAG) system in Python from scratch. The goal is to understand and implement the core components of a RAG pipeline manually, using Google AI components for convenience.

## Features

- **Chunking:** Split documents into manageable pieces.
- **Embedding:** Convert text chunks into vector representations.
- **Storing:** Save and manage embeddings for efficient retrieval.
- **Querying:** Retrieve relevant chunks based on user queries.

## Motivation

Constructing a RAG system by hand provides a deeper understanding of each step in the pipeline and offers flexibility for customization. Leveraging Google AI components streamlines the process and ensures high-quality results.

## Getting Started

1. Clone this repository.
2. Install dependencies (see `requirements.txt`).
3. Follow the code in each module to see how chunking, embedding, storing, and querying are implemented.

## Implementation Details

### 1. Chunking

- **Current:** Uses the simplest possible method to split documents into chunks.
- **Next:** Explore more advanced chunking strategies (e.g., sentence-based, overlap, semantic splitting).

### 2. Embedding

- **Current:** Utilizes Google Gemini AI's embedding model to convert text chunks into vectors.
- **Next:** Investigate alternative embedding models for comparison.

### 3. Vector Database

- **Current:** Stores embeddings locally using [ChromaDB](https://www.trychroma.com/).
- **Install ChromaDB:**
    ```bash
    pip install chromadb
    ```

### 4. API Authentication

- **Requirement:** Set your Google API token as an environment variable:
    ```bash
    export GOOGLE_API_KEY=your_token_here
    ```

## License

MIT License.