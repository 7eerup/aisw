from sqlalchemy.orm import Session
from models.memo import Memo


def find_all(db: Session, keyword: str | None = None, user_id=None):
    query = db.query(Memo)

    if user_id is not None:
        query = query.filter(Memo.user_id == user_id)

    if keyword:
        query = query.filter(
            Memo.title.like(f"%{keyword}%")
        )

    return query.order_by(Memo.id.desc()).all()


def find_by_id(db: Session, memo_id: int):
    return db.query(Memo).filter(Memo.id == memo_id).first()


def save(db, memo):
    db.add(memo)
    db.commit()
    db.refresh(memo)

    return memo


def update(db: Session, memo: Memo, title: str, content: str,  category_id=None):
    memo.title = title
    memo.content = content
    memo.category_id = category_id

    db.commit()
    db.refresh(memo)

    return memo


def update_status(db, memo, status):
    memo.status = status
    db.commit()
    db.refresh(memo)
    return memo


def delete(db: Session, memo: Memo):
    db.delete(memo)
    db.commit()