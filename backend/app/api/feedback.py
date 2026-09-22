from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.auth.dependencies import get_current_user
from backend.app.auth.roles import require_admin
from backend.app.database.connection import get_db
from backend.app.models.feedback import Feedback
from backend.app.models.user import User


router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    grounding_score: float
    feedback: str


@router.post("")
def submit_feedback(
    data: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.feedback not in ["helpful", "not_helpful"]:
        raise HTTPException(
            status_code=400,
            detail="Feedback must be helpful or not_helpful",
        )

    feedback = Feedback(
        user_id=current_user.id,
        question=data.question,
        answer=data.answer,
        grounding_score=data.grounding_score,
        feedback=data.feedback,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.id,
    }


@router.get("/analytics")
def get_feedback_analytics(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    total_feedback = db.scalar(
        select(func.count(Feedback.id))
    ) or 0

    helpful_count = db.scalar(
        select(func.count(Feedback.id))
        .where(Feedback.feedback == "helpful")
    ) or 0

    not_helpful_count = db.scalar(
        select(func.count(Feedback.id))
        .where(Feedback.feedback == "not_helpful")
    ) or 0

    average_grounding_score = db.scalar(
        select(func.avg(Feedback.grounding_score))
    )

    return {
        "total_feedback": total_feedback,
        "helpful": helpful_count,
        "not_helpful": not_helpful_count,
        "average_grounding_score": (
            round(float(average_grounding_score), 4)
            if average_grounding_score is not None
            else 0.0
        ),
    }