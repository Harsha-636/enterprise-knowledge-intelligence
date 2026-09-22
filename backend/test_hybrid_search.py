from sqlalchemy.orm import Session

from backend.app.database.connection import engine
from backend.app.retrieval.hybrid_search import hybrid_search


db = Session(engine)

results = hybrid_search(
    db=db,
    query="What programming skills does Harsha have?",
    top_k=3,
)

for result in results:
    print(
        f"Chunk: {result['chunk_id']} | "
        f"Semantic: {result['semantic_score']:.4f} | "
        f"Keyword: {result['keyword_score']:.4f} | "
        f"Final: {result['score']:.4f}"
    )

db.close()