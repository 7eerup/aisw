from sqlalchemy.orm import Session

from models.category import Category


def find_all(db: Session):
    return db.query(Category).order_by(Category.name).all()


def find_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()