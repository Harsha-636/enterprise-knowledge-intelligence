from sqlalchemy.orm import Session

from backend.app.generation.llm_service import generate_answer
from backend.app.retrieval.query_rewriter import rewrite_query
from backend.app.retrieval.hybrid_search import hybrid_search
from backend.app.retrieval.reranker import rerank


def answer_question(
    db: Session,
    question: str,
    user_id: int,
    top_k: int = 3,
) -> dict:

    # Step 1: Rewrite the user's question
    rewritten_query = rewrite_query(question)

    # Step 2: Retrieve only this user's documents
    candidates = hybrid_search(
        db=db,
        query=rewritten_query,
        user_id=user_id,
        top_k=10,
    )

    if not candidates:
        return {
            "answer": (
                "I could not find this information "
                "in the available documents."
            ),
            "sources": [],
            "rewritten_query": rewritten_query,
        }

    # Step 3: Rerank retrieved candidates
    results = rerank(
        query=question,
        results=candidates,
        top_k=top_k,
    )

    # Step 4: Build context
    context_parts = []

    for result in results:
        context_parts.append(
            f"[Chunk {result['chunk_id']}]\n"
            f"{result['content']}"
        )

    context = "\n\n".join(context_parts)

    # Step 5: Generate grounded answer
    answer = generate_answer(
        question=question,
        context=context,
    )

    # Step 6: Return answer and sources
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
    }