from sqlalchemy.orm import Session

from backend.app.database.connection import engine
from backend.app.services.rag_service import answer_question


db = Session(engine)

result = answer_question(
    db=db,
    question="What programming skills does Harsha have?",
)

print("\nREWRITTEN QUERY:")
print(result["rewritten_query"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")

for source in result["sources"]:
    print(
        f"Chunk: {source['chunk_id']} | "
        f"Hybrid: {source['score']:.4f} | "
        f"Rerank: {source['rerank_score']:.4f}"
    )

db.close()