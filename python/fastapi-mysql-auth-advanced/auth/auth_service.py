from fastapi import Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from services import user_service


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User | None:
    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    user = user_service.get_user(
        db=db,
        user_id=user_id,
    )

    if user is None:
        request.session.clear()
        return None

    return user


def require_login(
    current_user: User | None = Depends(get_current_user),
) -> User | None:
    return current_user