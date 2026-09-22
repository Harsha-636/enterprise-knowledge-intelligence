from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(MODEL_NAME)


def rerank(
    query: str,
    results: list[dict],
    top_k: int = 3,
) -> list[dict]:

    if not results:
        return []

    pairs = [
        (query, result["content"])
        for result in results
    ]

    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):
        item = result.copy()
        item["rerank_score"] = float(score)
        reranked.append(item)

    reranked.sort(
        key=lambda item: item["rerank_score"],
        reverse=True,
    )

    return reranked[:top_k]