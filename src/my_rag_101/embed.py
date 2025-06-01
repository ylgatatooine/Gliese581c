import sys
import chunk

import chromadb
from chromadb import PersistentClient
from chromadb.api import ClientAPI, Collection

from typing import Any

from google import genai
from google.genai.types import GenerateContentResponse

from params import EMBEDDING_MODEL, LLM_MODEL  # <-- updated import

google_client = genai.Client()

chromadb_client: ClientAPI = chromadb.PersistentClient('./chroma.db')
chromadb_collection: Collection = chromadb_client.get_or_create_collection('ylg_first_embedding_col')

def embed(text: str, store: bool) -> list[float]:
    """
    Dummy embedding function. Replace with real embedding logic.
    """
    result: EmbedContentResponse = google_client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents = text,
        config = {
            'task_type' : 'RETRIEVAL_DOCUMENT' if store else 'RETRIEVAL_QUERY'
        }
    )

    assert result.embeddings
    assert result.embeddings[0].values
    return result.embeddings[0].values

def create_db() -> None:
    for idx, c in enumerate(chunk.get_chunks()):
        print(f'Process: {c}')
        embedding: list[float] = embed(c, store=True)
        chromadb_collection.upsert(
            ids = str(idx),
            documents = c,
            embeddings = embedding
        )

def query_db(question: str) -> list[str]:
    question_embedding: list[float] = embed(question, store = False)
    result: QueryResult = chromadb_collection.query(
        query_embeddings = question_embedding, 
        n_results = 5
    )
    assert result['documents']
    return result['documents'][0]

if __name__ == '__main__':

    question = 'Geoffrey becomes a great magician.'
    chunks: list[str] = query_db(question)
    prompt = 'Please answer the question according to context\n'
    prompt += f'Question: {question}\n'
    prompt += 'Context: \n'
    for c in chunks:
        prompt += f"{c}\n"
        prompt += "------------\n"

    result: GenerateContentResponse = google_client.models.generate_content(
        model = LLM_MODEL,
        contents = prompt
    )

    # Extract only the useful answer text from the result
    # This assumes the result object has a .candidates list with .content.parts[0].text
    useful_text = ""
    try:
        candidates = result.candidates
        if candidates and hasattr(candidates[0], "content"):
            parts = getattr(candidates[0].content, "parts", [])
            if parts and hasattr(parts[0], "text"):
                useful_text = parts[0].text
    except Exception as e:
        useful_text = f"Could not extract answer: {e}"

    print("Extracted Answer:\n")
    print(useful_text)

    # step 5: generate the result from LLM
    #
    # print(result)

    # step 4: Test what prompt is
    #
    # print(prompt)

    # step 3: Test Query vector DB 
    #
    #  chunks: list[str] = query_db(question)
    #  for c in chunks:
    #     print(c)
    #     print('-------------')

    # step 2: Test creating vector DB
    # create_db()

    # step 1: Test finding chunks from embedding from vector DB
    #
    # chunks: list[str] = chunk.get_chunks()
    # print(embed(chunks[0], True))