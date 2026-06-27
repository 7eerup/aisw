from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from services import user_service
from auth import auth_service

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": None}
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    db: Session = Depends(get_db),
):
    user = user_service.authenticate_user(db, username, password)

    if user is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "아이디 또는 비밀번호가 올바르지 않습니다."}
        )

    auth_service.login_user(request, user)

    return RedirectResponse(
        url="/memos",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/logout")
def logout(request: Request):
    auth_service.logout_user(request)

    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER
    )