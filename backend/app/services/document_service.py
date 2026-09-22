from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from backend.app.models.document import Document
from backend.app.services.chunk_service import create_document_chunks
from backend.app.services.embedding_pipeline import embed_document_chunks


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_document(
    db: Session,
    filename: str,
    file_bytes: bytes,
    uploaded_by: int,
) -> Document:

    file_path = UPLOAD_DIR / filename
    file_path.write_bytes(file_bytes)

    reader = PdfReader(str(file_path))

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    document = Document(
        filename=filename,
        file_path=str(file_path),
        content=extracted_text,
        status="processed",
        uploaded_by=uploaded_by,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Create chunks
    create_document_chunks(
        db=db,
        document=document,
    )

    # Create embeddings
    embed_document_chunks(
        db=db,
        document_id=document.id,
    )

    return document