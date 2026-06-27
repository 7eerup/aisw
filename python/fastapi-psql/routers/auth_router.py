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


@router.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse(
        request,
        "signup.html",
        {"error": None}
    )


@router.post("/signup")
def signup(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    name: str = Form(""),
    db: Session = Depends(get_db),
):
    if not username.strip():
        return templates.TemplateResponse(request, "signup.html", {"error": "아이디는 필수입니다."})

    if not password.strip():
        return templates.TemplateResponse(request, "signup.html", {"error": "비밀번호는 필수입니다."})

    if not name.strip():
        return templates.TemplateResponse(request, "signup.html", {"error": "이름은 필수입니다."})

    existing_user = user_service.get_user_by_username(db, username)

    if existing_user:
        return templates.TemplateResponse(request, "signup.html", {"error": "이미 사용 중인 아이디입니다."})

    user_service.create_user(db, username, password, name)

    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER
    )