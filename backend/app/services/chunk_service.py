from sqlalchemy.orm import Session

from backend.app.models.chunk import Chunk
from backend.app.models.document import Document
from backend.app.services.chunking_service import chunk_text


def create_document_chunks(
    db: Session,
    document: Document,
) -> list[Chunk]:
    chunks = chunk_text(document.content or "")

    chunk_records = []

    for index, content in enumerate(chunks):
        chunk = Chunk(
            document_id=document.id,
            content=content,
            chunk_index=index,
        )

        db.add(chunk)
        chunk_records.append(chunk)

    db.commit()

    return chunk_records