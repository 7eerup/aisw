from sqlalchemy import select
from sqlalchemy.orm import Session

from models.memo import Memo


def get_memos(db: Session, user_id: int, keyword: str | None = None) -> list[Memo]:

    statement = select(Memo).where(
        Memo.user_id == user_id,
    )

    if keyword:
        statement = statement.where(Memo.title.like(f"%{keyword}%"))

    statement = statement.order_by(Memo.id.desc())
    return list(db.scalars(statement).all())


def get_memo(db: Session, memo_id: int, user_id: int) -> Memo | None:
    statement = select(Memo).where(
        Memo.id == memo_id,
        Memo.user_id == user_id,
    )

    return db.scalar(statement)


def create_memo(
    db: Session,
    title: str,
    content: str,
    user_id: int,
    category_id: int | None = None,
) -> Memo:
    memo = Memo(
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id,
    )

    db.add(memo)
    db.commit()
    db.refresh(memo)

    return memo


def update_memo(
    db: Session,
    memo: Memo,
    title: str,
    content: str,
    category_id: int | None = None,
) -> Memo:
    memo.title = title
    memo.content = content
    memo.category_id = category_id

    db.commit()
    db.refresh(memo)

    return memo


def toggle_status(
    db: Session,
    memo: Memo,
) -> Memo:
    if memo.status == "done":
        memo.status = "todo"
    else:
        memo.status = "done"

    db.commit()
    db.refresh(memo)

    return memo


def delete_memo(
    db: Session,
    memo: Memo,
) -> None:
    db.delete(memo)
    db.commit()
