from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.auth.jwt import create_access_token
from backend.app.database.connection import get_db
from backend.app.schemas.user import UserCreate, UserResponse
from backend.app.services.user_service import (
    authenticate_user,
    create_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_user(db, user.email, user.password)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
def login(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    authenticated_user = authenticate_user(
        db,
        user.email,
        user.password,
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        authenticated_user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }