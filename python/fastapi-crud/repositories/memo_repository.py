from sqlalchemy.orm import Session
from models.memo import Memo


def find_all(db: Session):
    return db.query(Memo).order_by(Memo.id.desc()).all()


def find_by_id(db: Session, memo_id: int):
    return db.query(Memo).filter(Memo.id == memo_id).first()


def save(db: Session, title: str, content: str):
    memo = Memo(title=title, content=content)

    db.add(memo)
    db.commit()
    db.refresh(memo)

    return memo


def update(db: Session, memo: Memo, title: str, content: str):
    memo.title = title
    memo.content = content

    db.commit()
    db.refresh(memo)

    return memo


def delete(db: Session, memo: Memo):
    db.delete(memo)
    db.commit()