from sqlalchemy.orm import Session

from backend.app.models.chunk import Chunk
from backend.app.models.document import Document
from backend.app.services.embedding_service import create_embedding
from backend.app.retrieval.similarity import cosine_similarity
from backend.app.retrieval.vector_store import load_embeddings


def search_chunks(
    db: Session,
    query: str,
    user_id: int,
    top_k: int = 3,
) -> list[dict]:

    query_embedding = create_embedding(query)

    stored_embeddings = load_embeddings()

    results = []

    for chunk_id, embedding in stored_embeddings.items():

        chunk = db.get(Chunk, int(chunk_id))

        if not chunk:
            continue

        document = db.get(Document, chunk.document_id)

        if not document:
            continue

        # Security: only search documents owned by this user
        if document.uploaded_by != user_id:
            continue

        score = cosine_similarity(
            query_embedding,
            embedding,
        )

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