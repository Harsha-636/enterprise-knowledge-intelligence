from sqlalchemy.orm import Session

from backend.app.retrieval.search import search_chunks
from backend.app.retrieval.keyword_search import keyword_search


def hybrid_search(
    db: Session,
    query: str,
    user_id: int,
    top_k: int = 3,
) -> list[dict]:

    semantic_results = search_chunks(
        db=db,
        query=query,
        user_id=user_id,
        top_k=top_k,
    )

    keyword_results = keyword_search(
        db=db,
        query=query,
        user_id=user_id,
        top_k=top_k,
    )

    combined = {}

    for result in semantic_results:
        chunk_id = result["chunk_id"]

        combined[chunk_id] = {
            "chunk_id": chunk_id,
            "document_id": result["document_id"],
            "content": result["content"],
            "semantic_score": result["score"],
            "keyword_score": 0.0,
        }

    for result in keyword_results:
        chunk_id = result["chunk_id"]

        if chunk_id not in combined:
            combined[chunk_id] = {
                "chunk_id": chunk_id,
                "document_id": result["document_id"],
                "content": result["content"],
                "semantic_score": 0.0,
                "keyword_score": result["score"],
            }
        else:
            combined[chunk_id]["keyword_score"] = result["score"]

    results = []

    for result in combined.values():
        final_score = (
            0.7 * result["semantic_score"]
            + 0.3 * result["keyword_score"]
        )

        result["score"] = final_score
        results.append(result)

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]