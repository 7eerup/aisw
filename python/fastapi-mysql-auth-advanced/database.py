import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")

if MYSQL_DATABASE_URL is None:
    raise RuntimeError("MYSQL_DATABASE_URL 환경 변수가 설정되지 않았습니다.")

if MYSQL_DATABASE_URL.startswith("mysql://"):
    MYSQL_DATABASE_URL = MYSQL_DATABASE_URL.replace(
        "mysql://",
        "mysql+pymysql://",
        1,
    )

engine = create_engine(MYSQL_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
