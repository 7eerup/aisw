from sqlalchemy.orm import Session
from repositories import memo_repository


def get_memos(db: Session, keyword: str | None = None):
    return memo_repository.find_all(db, keyword)


def get_memo(db: Session, memo_id: int):
    return memo_repository.find_by_id(db, memo_id)


def create_memo(db: Session, title: str, content: str):
    if not title.strip():
        raise ValueError(
            "제목은 필수 입력입니다."
        )

    if not content.strip():
        raise ValueError(
            "내용은 필수 입력입니다."
        )
    
    return memo_repository.save(db, title, content)


def update_memo(db: Session, memo_id: int, title: str, content: str):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return None

    return memo_repository.update(db, memo, title, content)


def delete_memo(db: Session, memo_id: int):
    memo = memo_repository.find_by_id(db, memo_id)

    if memo is None:
        return False

    memo_repository.delete(db, memo)
    return True