from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.auth.dependencies import get_current_user
from backend.app.auth.roles import require_admin
from backend.app.database.connection import get_db
from backend.app.models.document import Document
from backend.app.models.user import User
from backend.app.services.document_service import save_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty",
        )

    document = save_document(
        db=db,
        filename=file.filename,
        file_bytes=file_bytes,
        uploaded_by=current_user.id,
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "status": document.status,
        "uploaded_by": document.uploaded_by,
        "document_type": document.document_type,
        "page_count": document.page_count,
        "word_count": document.word_count,
        "character_count": document.character_count,
    }


@router.get("")
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    documents = db.scalars(
        select(Document)
        .where(Document.uploaded_by == current_user.id)
        .order_by(Document.created_at.desc())
    ).all()

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "status": document.status,
            "uploaded_by": document.uploaded_by,
            "document_type": document.document_type,
            "page_count": document.page_count,
            "word_count": document.word_count,
            "character_count": document.character_count,
            "created_at": document.created_at,
        }
        for document in documents
    ]


@router.get("/admin/all")
def get_all_documents(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    documents = db.scalars(
        select(Document)
        .order_by(Document.created_at.desc())
    ).all()

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "status": document.status,
            "uploaded_by": document.uploaded_by,
            "document_type": document.document_type,
            "page_count": document.page_count,
            "word_count": document.word_count,
            "character_count": document.character_count,
            "created_at": document.created_at,
        }
        for document in documents
    ]