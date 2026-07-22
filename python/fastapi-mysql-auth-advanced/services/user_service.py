import secrets

from sqlalchemy.orm import Session

from auth.password import hash_password, verify_password
from models.user import User
from repositories import category_repository, user_repository


def create_user(
    db: Session,
    username: str,
    password: str,
    name: str,
) -> User:
    hashed_password = hash_password(password)

    user = user_repository.create_user(
        db=db,
        username=username,
        password=hashed_password,
        name=name,
    )

    category_repository.create_default_categories(
        db=db,
        user_id=user.id,
    )

    db.commit()
    db.refresh(user)

    return user


def create_oauth_user(
    db: Session,
    username: str,
    name: str,
) -> User:
    random_password = secrets.token_urlsafe(32)
    hashed_password = hash_password(random_password)

    user = user_repository.create_oauth_user(
        db=db,
        username=username,
        password=hashed_password,
        name=name,
    )

    category_repository.create_default_categories(
        db=db,
        user_id=user.id,
    )

    db.commit()
    db.refresh(user)

    return user


def get_user(
    db: Session,
    user_id: int,
) -> User | None:
    return user_repository.get_user(
        db=db,
        user_id=user_id,
    )


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    username = username.strip()

    if not username or not password:
        return None

    user = user_repository.get_user_by_username(
        db=db,
        username=username,
    )

    if user is None:
        return None

    if user.password is None:
        return None

    if not verify_password(
        password,
        user.password,
    ):
        return None

    return user
