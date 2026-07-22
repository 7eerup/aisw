import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from auth.auth_service import get_current_user
from database import Base, engine
from models.category import Category
from models.memo import Memo
from models.user import User
from routers import auth_router, memo_router
from services.memo_service import ResourceNotFoundError

load_dotenv()

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

if SESSION_SECRET_KEY is None:
    raise RuntimeError("SESSION_SECRET_KEY 환경 변수가 설정되지 않았습니다.")


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")


@app.exception_handler(ResourceNotFoundError)
def resource_not_found_handler(
    request: Request,
    exc: ResourceNotFoundError,
):

    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={
            "message": exc.message,
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={
                "message": "요청한 페이지를 찾을 수 없습니다.",
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


@app.get("/")
def home(
    request: Request,
    current_user: User | None = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "current_user": current_user,
        },
    )


@app.get("/logo")
def logo_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="logo.html",
        context={},
    )


app.include_router(auth_router.router)
app.include_router(memo_router.router)
