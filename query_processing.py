import time
from embedder import query_embed
from vectordb import search_in_pinecone
from RAG_llm import llm_query_context
from reranker import rerank

chat_history = []


def query_processor(query: str, use_rerank: bool = True):
    start = time.perf_counter()

    query_vector = query_embed(query)

    if use_rerank:
        candidates = search_in_pinecone(query_vector, top_k=20)  # retrieve wide
        matches = rerank(query, candidates, top_n=4)             # keep the best 4
    else:
        matches = search_in_pinecone(query_vector, top_k=4)

    context = "\n\n".join(matches)

    history_text = ""
    for history in chat_history[-3:]:   # only the last 3 turns, to save tokens
        history_text += f"User {history['user']}\nAssistance {history['assistance']}\n\n"

    full_history = history_text + context

    generated_response = llm_query_context(query, full_history)

    chat_history.append({
        'user': query,
        'assistance': generated_response
    })

    elapsed = time.perf_counter() - start
    print(f"Answer: {generated_response}")
    print(f"[{'with' if use_rerank else 'without'} reranking | {elapsed:.1f}s]")
    return generated_response


if __name__ == "__main__":
    use_rerank = True
    while True:
        query = input("You: ")
        cmd = query.lower().strip()
        if cmd == "exit":
            break
        if cmd == "rerank on":
            use_rerank = True
            print("Reranking is ON")
            continue
        if cmd == "rerank off":
            use_rerank = False
            print("Reranking is OFF")
            continue
        if cmd == "clear":
            chat_history.clear()
            print("History cleared")
            continue
        query_processor(query, use_rerank)
