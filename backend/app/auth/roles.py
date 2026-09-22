from fastapi import Depends, HTTPException, status

from backend.app.auth.dependencies import get_current_user
from backend.app.models.user import User


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    print(
        f"RBAC CHECK -> id={current_user.id}, "
        f"email={current_user.email}, "
        f"role={current_user.role}"
    )

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user