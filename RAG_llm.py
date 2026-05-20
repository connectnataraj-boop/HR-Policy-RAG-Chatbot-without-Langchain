from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def llm_query_context(query: str, context: str):

    system_content = """You are a helpfull assistance to provide answer based on user query from given context.
    use the context to provide accurate and relevent answer. Don't make assumption beyond the context porvided.
    If context does not contain enough information for the asked query, let the user know the you can't provide answer based on given context."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Query: {query}\n\nContext:\n{context}"},
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
