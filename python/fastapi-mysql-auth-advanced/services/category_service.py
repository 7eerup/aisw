from sqlalchemy.orm import Session

from models.category import Category
from repositories import category_repository


def get_categories(
    db: Session,
    user_id: int,
) -> list[Category]:
    return category_repository.get_categories(
        db=db,
        user_id=user_id,
    )


def get_category(
    db: Session,
    category_id: int,
    user_id: int,
) -> Category | None:
    return category_repository.get_category(
        db=db,
        category_id=category_id,
        user_id=user_id,
    )


def create_category(
    db: Session,
    name: str,
    user_id: int,
) -> Category:
    return category_repository.create_category(
        db=db,
        name=name,
        user_id=user_id,
    )