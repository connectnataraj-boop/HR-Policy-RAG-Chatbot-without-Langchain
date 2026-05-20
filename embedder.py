from openai import OpenAI
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = "text-embedding-3-small"


def embed_model(chunks: List[str]) -> List[List[float]]:

    embedding = []

    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model=EMBEDDING_MODEL
        )
        embedding.append(response.data[0].embedding)

    return embedding


def query_embed(query: str):

    response = client.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding
