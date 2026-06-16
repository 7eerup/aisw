from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from database import Base, engine
from models.memo import Memo
from models import category
from routers.memo_router import router as memo_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(memo_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {}
    )