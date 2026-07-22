from sqlalchemy import select
from sqlalchemy.orm import Session

from models.category import Category


def get_categories(
    db: Session,
    user_id: int,
) -> list[Category]:
    statement = (
        select(Category).where(Category.user_id == user_id).order_by(Category.id.asc())
    )

    return list(db.scalars(statement).all())


def get_category(
    db: Session,
    category_id: int,
    user_id: int,
) -> Category | None:
    statement = select(Category).where(
        Category.id == category_id,
        Category.user_id == user_id,
    )

    return db.scalar(statement)


def create_category(
    db: Session,
    name: str,
    user_id: int,
) -> Category:
    category = Category(
        name=name,
        user_id=user_id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def create_default_categories(
    db: Session,
    user_id: int,
) -> list[Category]:
    category_names = [
        "공부",
        "업무",
        "개인",
    ]

    categories = [
        Category(
            name=name,
            user_id=user_id,
        )
        for name in category_names
    ]

    db.add_all(categories)
    db.flush()

    return categories
