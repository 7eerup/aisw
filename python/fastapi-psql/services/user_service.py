from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user import User
from repositories import user_repository


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str):
    return pwd_context.hash(password)


def get_user_by_id(db: Session, user_id: int):
    return user_repository.find_by_id(db, user_id)


def get_user_by_username(db: Session, username: str):
    return user_repository.find_by_username(db, username)


def create_user(db: Session, username: str, password: str, name: str):
    user = User(
        username=username,
        password=hash_password(password),
        name=name,
    )

    return user_repository.save(db, user)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def authenticate_user(db: Session, username: str, password: str):
    user = user_repository.find_by_username(db, username)

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user