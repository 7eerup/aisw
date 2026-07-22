import httpx

from authlib.integrations.base_client.errors import OAuthError
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from auth.oauth_client import oauth
from database import get_db
from repositories import user_repository
from services import user_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/signup")
def signup_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={
            "error": None,
            "username": "",
            "name": "",
        },
    )


@router.post("/signup")
def signup(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    password_confirm: str = Form(""),
    name: str = Form(""),
    db: Session = Depends(get_db),
):
    username = username.strip()
    name = name.strip()

    context = {
        "error": None,
        "username": username,
        "name": name,
    }

    if not username:
        context["error"] = "아이디를 입력해 주세요."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if len(username) > 50:
        context["error"] = "아이디는 50자 이하로 입력해 주세요."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not name:
        context["error"] = "이름을 입력해 주세요."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if len(name) > 50:
        context["error"] = "이름은 50자 이하로 입력해 주세요."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not password:
        context["error"] = "비밀번호를 입력해 주세요."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if len(password) < 8:
        context["error"] = "비밀번호는 8자 이상으로 입력해 주세요."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if password != password_confirm:
        context["error"] = "비밀번호 확인이 일치하지 않습니다."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    existing_user = user_repository.get_user_by_username(
        db=db,
        username=username,
    )

    if existing_user is not None:
        context["error"] = "이미 사용 중인 아이디입니다."

        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context=context,
            status_code=status.HTTP_409_CONFLICT,
        )

    user_service.create_user(
        db=db,
        username=username,
        password=password,
        name=name,
    )

    return RedirectResponse(
        url="/login?signup=success",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/login")
def login_form(
    request: Request,
    signup: str | None = None,
    error: str | None = None,
):
    error_messages = {
        "github_oauth_failed": "GitHub 인증에 실패했습니다.",
        "github_user_info_failed": "GitHub 사용자 정보를 가져오지 못했습니다.",
        "google_oauth_failed": "Google 인증에 실패했습니다.",
        "google_user_info_failed": "Google 사용자 정보를 가져오지 못했습니다.",
        "google_email_missing": "Google 이메일 정보를 가져오지 못했습니다.",
    }

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "success": ("회원가입이 완료되었습니다." if signup == "success" else None),
            "error": error_messages.get(error),
        },
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    db: Session = Depends(get_db),
):
    user = user_service.authenticate_user(
        db=db,
        username=username,
        password=password,
    )

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "아이디 또는 비밀번호가 올바르지 않습니다.",
                "username": username,
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.session.clear()
    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/memos",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/auth/github")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")

    return await oauth.github.authorize_redirect(
        request,
        redirect_uri,
    )


@router.get(
    "/auth/github/callback",
    name="github_callback",
)
async def github_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = await oauth.github.authorize_access_token(request)

        response = await oauth.github.get(
            "user",
            token=token,
        )
        response.raise_for_status()

    except (OAuthError, httpx.HTTPStatusError):
        return RedirectResponse(
            url="/login?error=github_oauth_failed",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    github_user = response.json()
    username = github_user.get("login")

    if not username:
        return RedirectResponse(
            url="/login?error=github_user_info_failed",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    name = github_user.get("name") or username

    user = user_repository.get_user_by_username(
        db=db,
        username=username,
    )

    if user is None:
        user = user_service.create_oauth_user(
            db=db,
            username=username,
            name=name,
        )

    request.session.clear()
    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/memos",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )


@router.get(
    "/auth/google/callback",
    name="google_callback",
)
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        token = await oauth.google.authorize_access_token(request)

    except OAuthError:
        return RedirectResponse(
            url="/login?error=google_oauth_failed",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    user_info = token.get("userinfo")

    if user_info is None:
        return RedirectResponse(
            url="/login?error=google_user_info_failed",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    email = user_info.get("email")

    if not email:
        return RedirectResponse(
            url="/login?error=google_email_missing",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    email = email.strip().lower()
    name = user_info.get("name") or email

    user = user_repository.get_user_by_username(
        db=db,
        username=email,
    )

    if user is None:
        user = user_service.create_oauth_user(
            db=db,
            username=email,
            name=name,
        )

    request.session.clear()
    request.session["user_id"] = user.id

    return RedirectResponse(
        url="/memos",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
