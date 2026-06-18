from sqlalchemy.orm import Session
from repositories import memo_repository


def get_memos(db: Session, keyword: str | None = None, category_id: int | None = None):
    return memo_repository.find_all(db, keyword, category_id)


def get_memo(db: Session, memo_id: int):
    return memo_repository.find_by_id(db, memo_id)


def create_memo(db: Session, title: str, content: str, category_id: int | None = None):
    return memo_repository.save(db, title, content, category_id)


def update_memo(db: Session, memo_id: int, title: str, content: str, category_id: int | None = None):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return None

    return memo_repository.update(db, memo, title, content, category_id)


def delete_memo(db: Session, memo_id: int):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return False

    memo_repository.delete(db, memo)
    return True