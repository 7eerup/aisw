from sqlalchemy.orm import Session

from models.memo import Memo
from repositories import memo_repository


class ResourceNotFoundError(Exception):
    def __init__(
        self,
        message: str = "요청한 데이터를 찾을 수 없습니다.",
    ):
        self.message = message
        super().__init__(message)


def get_memo_or_raise(
    db: Session,
    memo_id: int,
    user_id: int,
) -> Memo:
    memo = memo_repository.get_memo(
        db=db,
        memo_id=memo_id,
        user_id=user_id,
    )

    if memo is None:
        raise ResourceNotFoundError("해당 메모를 찾을 수 없습니다.")

    return memo


def get_memos(
    db: Session,
    user_id: int,
    keyword: str | None = None,
) -> list[Memo]:
    return memo_repository.get_memos(
        db=db,
        user_id=user_id,
        keyword=keyword,
    )


def get_memo(
    db: Session,
    memo_id: int,
    user_id: int,
) -> Memo | None:
    return memo_repository.get_memo(
        db=db,
        memo_id=memo_id,
        user_id=user_id,
    )


def create_memo(
    db: Session,
    title: str,
    content: str,
    user_id: int,
    category_id: int | None = None,
) -> Memo:
    title = title.strip()
    content = content.strip()

    if not title:
        raise ValueError("제목을 입력해 주세요.")

    if not content:
        raise ValueError("내용을 입력해 주세요.")

    return memo_repository.create_memo(
        db=db,
        title=title,
        content=content,
        user_id=user_id,
        category_id=category_id,
    )


def update_memo(
    db: Session,
    memo_id: int,
    user_id: int,
    title: str,
    content: str,
    category_id: int | None = None,
) -> Memo:
    memo = get_memo_or_raise(db, memo_id, user_id=user_id)

    title = title.strip()
    content = content.strip()

    if not title:
        raise ValueError("제목을 입력해 주세요.")

    if not content:
        raise ValueError("내용을 입력해 주세요.")

    return memo_repository.update_memo(
        db=db,
        memo=memo,
        title=title,
        content=content,
        category_id=category_id,
    )


def toggle_memo_status(
    db: Session,
    memo_id: int,
    user_id: int,
) -> Memo:
    memo = get_memo_or_raise(
        db=db,
        memo_id=memo_id,
        user_id=user_id,
    )

    return memo_repository.toggle_status(
        db=db,
        memo=memo,
    )


def delete_memo(
    db: Session,
    memo_id: int,
    user_id: int,
) -> None:
    memo = get_memo_or_raise(db, memo_id, user_id=user_id)

    memo_repository.delete_memo(
        db=db,
        memo=memo,
    )
