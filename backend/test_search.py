from sqlalchemy.orm import Session

from backend.app.database.connection import engine
from backend.app.retrieval.search import search_chunks


db = Session(engine)

results = search_chunks(
    db,
    "What programming skills does Harsha have?",
    3,
)

for result in results:
    print(
        f"Chunk {result['chunk_id']} "
        f"| Score: {result['score']:.4f}"
    )

    print(result["content"][:300])
    print("---")

db.close()