from sqlalchemy.orm import Session

from models.user import User


def find_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def find_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def save(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user