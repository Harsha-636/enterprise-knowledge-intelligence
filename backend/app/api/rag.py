from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.auth.dependencies import get_current_user
from backend.app.database.connection import get_db
from backend.app.models.user import User
from backend.app.services.rag_service import answer_question


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


class QuestionRequest(BaseModel):
    question: str


@router.post("/query")
def query_knowledge(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = answer_question(
        db=db,
        question=request.question,
        user_id=current_user.id,
    )

    return result