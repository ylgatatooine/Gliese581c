import ollama
import chromadb
from chromadb import PersistentClient
from chromadb.api import ClientAPI, Collection

# Initialize ChromaDB client and collection
chromadb_client: ClientAPI = PersistentClient('./chroma.db')
chromadb_collection: Collection = chromadb_client.get_or_create_collection('ylg_first_embedding_col')

# Load the dataset from a text file
with open('cat-facts.txt', 'r') as file:
    dataset = file.readlines()
    print(f'Loaded {len(dataset)} entries')

# Model configuration for embedding and language model
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

# Embedding function using Ollama
# Returns a list of floats representing the embedding for the input text
def embed(text: str) -> list[float]:
    """
    Generate embedding for the given text using Ollama.
    """
    result = ollama.embed(model=EMBEDDING_MODEL, input=text)['embeddings'][0]
    return result

# Create or update the ChromaDB database from the dataset
# If the collection already contains data, skip creation
def update_vector_db() -> None:
    # if chromadb_collection.count() > 0:
    #     print('Database already exists. Skipping creation.')
    #     return

    for idx, c in enumerate(dataset):
        print(f'\rAdding chunk {idx+1}/{len(dataset)} to the database', end='', flush=True)
        embedding: list[float] = embed(c)
        chromadb_collection.upsert(
            ids=str(idx),
            documents=c,
            embeddings=embedding
        )

# Query the ChromaDB collection for the most relevant chunks given a question
def query_db(question: str, n_results: int = 5) -> list[str]:
    question_embedding: list[float] = embed(question)
    result = chromadb_collection.query(
        query_embeddings=question_embedding,
        n_results=n_results
    )
    assert result['documents']
    return result['documents'][0]

if __name__ == '__main__':
    # Only create the database if it doesn't already exist
    update_vector_db()

    # Example question for the chatbot
    # question = 'How many kinds of cat are there in the world?'
    question = input('\nAsk me a question: ')
    input_query = f'Question: {question}\n'

    # Retrieve relevant chunks from the database
    chunks: list[str] = query_db(question)
    instruction_prompt = (
        'You are a helpful chatbot. Use only the following pieces of context to answer the question. '
        'Do not make up any new information.\nContext:\n'
    )
    for c in chunks:
        instruction_prompt += f"{c}\n------------\n"

    # Start a chat session with the language model using the retrieved context
    stream = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {'role': 'system', 'content': instruction_prompt},
            {'role': 'user', 'content': input_query},
        ],
        stream=True,
    )

    # Print the response from the chatbot in real-time
    print('Chatbot response:')
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)