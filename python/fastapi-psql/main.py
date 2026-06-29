import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from database import Base, engine
from models.memo import Memo
from models.user import User
from models.category import Category

from routers.memo_router import router as memo_router
from routers.auth_router import router as auth_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
)

templates = Jinja2Templates(directory="templates")

app.include_router(memo_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {}
    )