from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


def create_user(
    db: Session,
    username: str,
    password: str,
    name: str,
) -> User:
    user = User(
        username=username,
        password=password,
        name=name,
    )

    db.add(user)
    db.flush()

    return user


def create_oauth_user(
    db: Session,
    username: str,
    password: str,
    name: str,
) -> User:
    user = User(
        username=username,
        password=password,
        name=name,
    )

    db.add(user)
    db.flush()

    return user


def get_user(
    db: Session,
    user_id: int,
) -> User | None:
    return db.get(User, user_id)


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)

    return db.scalar(statement)
