from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Commit:
    """변경할 수 없는 커밋과 해당 커밋의 부모 참조를 나타낸다."""

    hash: str
    message: str
    author: str
    timestamp: datetime
    parents: tuple[str, ...]
