from sqlalchemy.orm import Session
from repositories import category_repository


def get_categories(db: Session):
    return category_repository.find_all(db)