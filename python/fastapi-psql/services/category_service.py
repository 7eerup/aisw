from sqlalchemy.orm import Session

from repositories import category_repository


def get_categories(db: Session):
    return category_repository.find_all(db)


def get_category(db: Session, category_id: int):
    return category_repository.find_by_id(db, category_id)