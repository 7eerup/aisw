from sqlalchemy.orm import Session
from models.memo import Memo


def find_all(db: Session, keyword: str | None = None, category_id: int | None = None):
    query = db.query(Memo)

    if keyword:
        query = query.filter(
            Memo.title.like(f"%{keyword}%")
        )

    if category_id:
        query = query.filter(Memo.category_id == category_id)

    return query.order_by(Memo.id.desc()).all()


def find_by_id(db: Session, memo_id: int):
    return db.query(Memo).filter(Memo.id == memo_id).first()


def save(db: Session, title: str, content: str, category_id: int | None = None):
    memo = Memo(title=title, content=content, category_id=category_id)

    db.add(memo)
    db.commit()
    db.refresh(memo)

    return memo


def update(db: Session, memo: Memo, title: str, content: str, category_id: int | None = None):
    memo.title = title
    memo.content = content
    memo.category_id = category_id

    db.commit()
    db.refresh(memo)

    return memo


def delete(db: Session, memo: Memo):
    db.delete(memo)
    db.commit()