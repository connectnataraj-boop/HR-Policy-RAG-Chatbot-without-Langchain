from pinecone import Pinecone
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

pinecone_clint = Pinecone(api_key=os.getenv("Pinecone_API_KEY"))
index = pinecone_clint.Index(os.getenv("Pinecone_index_name"))


def pinecone_upsert(chunks: List[str], embeddings: List[List[float]], namespace: str = ""):
    vector_to_upsert = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vector = {
            "id": f'chunk {i}',
            "values": embedding,
            "metadata": {
                "text": chunk,
                "chunk_index": i
            }

        }
        vector_to_upsert.append(vector)

    batch_size = 100
    for i in range(0, len(vector_to_upsert), batch_size):
        batch = vector_to_upsert[i:i+batch_size]
        index.upsert(vector=batch, namespace=namespace)


def search_in_pinecone(query_vector: List[float], top_k=4, namespace: str = ""):
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    print(f'Found {len(results.matches)} matches in query')
    matches_found = []
    for match in results.matches:
        matches_found.append(match.metadata.get("text", ""))
    return matches_found
