from fastapi import APIRouter, Depends

from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User
from backend.app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user