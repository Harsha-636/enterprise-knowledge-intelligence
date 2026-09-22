from sqlalchemy.orm import Session

from backend.app.generation.llm_service import generate_answer
from backend.app.retrieval.query_rewriter import rewrite_query
from backend.app.retrieval.hybrid_search import hybrid_search
from backend.app.retrieval.reranker import rerank
from backend.app.services.grounding_service import validate_grounding


def answer_question(
    db: Session,
    question: str,
    user_id: int,
    top_k: int = 3,
) -> dict:

    rewritten_query = rewrite_query(question)

    candidates = hybrid_search(
        db=db,
        query=rewritten_query,
        user_id=user_id,
        top_k=10,
    )

    if not candidates:
        return {
            "answer": "I could not find this information in the available documents.",
            "sources": [],
            "rewritten_query": rewritten_query,
            "grounding": {
                "grounded": False,
                "score": 0.0,
                "reason": "No supporting documents found",
            },
        }

    results = rerank(
        query=question,
        results=candidates,
        top_k=top_k,
    )

    context_parts = []

    for result in results:
        context_parts.append(
            f"[Chunk {result['chunk_id']}]\n{result['content']}"
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question=question,
        context=context,
    )

    grounding = validate_grounding(
        answer=answer,
        context=context,
    )

    if not grounding["grounded"]:
        answer = (
            "I could not verify this answer from the available "
            "document context."
        )

    sources = [
        {
            "chunk_id": result["chunk_id"],
            "document_id": result["document_id"],
            "score": result["score"],
            "semantic_score": result["semantic_score"],
            "keyword_score": result["keyword_score"],
            "rerank_score": result["rerank_score"],
            "content": result["content"],
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources,
        "rewritten_query": rewritten_query,
        "grounding": grounding,
    }