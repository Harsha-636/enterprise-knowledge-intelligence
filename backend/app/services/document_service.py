from pathlib import Path
from uuid import uuid4

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

    original_filename = Path(filename).name
    safe_filename = f"{uuid4().hex}_{original_filename}"

    file_path = UPLOAD_DIR / safe_filename
    file_path.write_bytes(file_bytes)

    reader = PdfReader(str(file_path))

    extracted_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    page_count = len(reader.pages)
    word_count = len(extracted_text.split())
    character_count = len(extracted_text)

    document = Document(
        filename=original_filename,
        file_path=str(file_path),
        content=extracted_text,
        status="processed",
        uploaded_by=uploaded_by,
        document_type="pdf",
        page_count=page_count,
        word_count=word_count,
        character_count=character_count,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    create_document_chunks(
        db=db,
        document=document,
    )

    embed_document_chunks(
        db=db,
        document_id=document.id,
    )

    return document