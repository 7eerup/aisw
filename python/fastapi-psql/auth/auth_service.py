from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from services import user_service


def login_user(request: Request, user):
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["name"] = user.name


def logout_user(request: Request):
    request.session.clear()


def get_current_user(request: Request, db):
    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    return user_service.get_user_by_id(db, user_id)


def is_logged_in(request: Request):
    return request.session.get("user_id") is not None