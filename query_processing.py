from embedder import query_embed
from vectordb import search_in_pinecone
from RAG_llm import llm_query_context

chat_history = []


def query_processor(query: str):

    query_vector = query_embed(query)

    matches = search_in_pinecone(query_vector)
    context = "\n\n".join(matches)

    history_text = ""
    for history in chat_history:
        history_text += f"User {history['user']}\nAssistance {history['assistance']}\n\n"

    full_history = history_text+context

    generated_response = llm_query_context(query, full_history)

    chat_history.append({
        'user': query,
        'assistance': generated_response
    })
    print(f"Answer {generated_response}")


if __name__ == "__main__":
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        query_processor(query)
