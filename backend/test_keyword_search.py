from sqlalchemy.orm import Session

from backend.app.database.connection import engine
from backend.app.retrieval.keyword_search import keyword_search


db = Session(engine)

results = keyword_search(
    db=db,
    query="What programming skills does Harsha have?",
    top_k=3,
)

for result in results:
    print(
        f"Chunk: {result['chunk_id']} | "
        f"Score: {result['score']:.4f}"
    )

db.close()