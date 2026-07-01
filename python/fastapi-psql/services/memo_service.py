from sqlalchemy.orm import Session

from models.memo import Memo
from repositories import memo_repository


def get_memos(db: Session, keyword: str | None = None, user_id: int | None = None):
    return memo_repository.find_all(db, keyword, user_id)


def get_memo(db: Session, memo_id: int):
    return memo_repository.find_by_id(db, memo_id)


def create_memo(db, title, content, user_id, category_id=None):
    if not title.strip():
        raise ValueError("제목은 필수 입력입니다.")

    if not content.strip():
        raise ValueError("내용은 필수 입력입니다.")

    memo = Memo(
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id,
    )
    
    return memo_repository.save(db, memo)


def update_memo(db: Session, memo_id: int, title: str, content: str, category_id=None):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return None

    return memo_repository.update(db, memo, title, content, category_id)


def toggle_memo_status(db, memo_id: int):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return None

    new_status = "done" if memo.status == "draft" else "draft"

    return memo_repository.update_status(db, memo, new_status)


def delete_memo(db: Session, memo_id: int):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return False

    memo_repository.delete(db, memo)
    return True