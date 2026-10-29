from sentence_transformers import CrossEncoder

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _model


def rerank(query, chunks, top_n=4):
    """chunks: a list of text strings. Returns the best top_n strings."""
    if len(chunks) <= top_n:
        return chunks
    try:
        model = _get_model()
        scores = model.predict([(query, c) for c in chunks])
        ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
        return [c for _, c in ranked[:top_n]]
    except Exception as e:
        print(f"Rerank failed, using vector order: {e}")
        return chunks[:top_n]
