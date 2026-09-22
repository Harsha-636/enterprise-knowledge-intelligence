from sqlalchemy.orm import Session

from backend.app.models.chunk import Chunk
from backend.app.services.embedding_service import create_embedding
from backend.app.retrieval.vector_store import save_embedding


def embed_document_chunks(
    db: Session,
    document_id: int,
) -> int:
    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .all()
    )

    count = 0

    for chunk in chunks:
        embedding = create_embedding(chunk.content)

        save_embedding(
            chunk_id=chunk.id,
            embedding=embedding,
        )

        count += 1

    return count