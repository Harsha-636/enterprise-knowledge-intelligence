import re

from sqlalchemy.orm import Session

from backend.app.models.chunk import Chunk
from backend.app.models.document import Document


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b\w+\b", text.lower())


def keyword_search(
    db: Session,
    query: str,
    user_id: int,
    top_k: int = 3,
) -> list[dict]:

    query_words = set(tokenize(query))

    chunks = (
        db.query(Chunk)
        .join(Document, Chunk.document_id == Document.id)
        .filter(Document.uploaded_by == user_id)
        .all()
    )

    results = []

    for chunk in chunks:

        chunk_words = set(tokenize(chunk.content))

        matches = query_words.intersection(chunk_words)

        if query_words:
            score = len(matches) / len(query_words)
        else:
            score = 0.0

        if score > 0:
            results.append({
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "score": score,
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]