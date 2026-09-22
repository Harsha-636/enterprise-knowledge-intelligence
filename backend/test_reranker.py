from sqlalchemy.orm import Session

from backend.app.database.connection import engine
from backend.app.retrieval.hybrid_search import hybrid_search
from backend.app.retrieval.reranker import rerank


db = Session(engine)

query = "What programming skills does Harsha have?"

results = hybrid_search(
    db=db,
    query=query,
    top_k=3,
)

reranked_results = rerank(
    query=query,
    results=results,
    top_k=3,
)

print("\nRERANKED RESULTS:\n")

for result in reranked_results:
    print(
        f"Chunk: {result['chunk_id']} | "
        f"Hybrid: {result['score']:.4f} | "
        f"Rerank: {result['rerank_score']:.4f}"
    )

db.close()