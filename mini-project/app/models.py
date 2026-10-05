from dataclasses import dataclass


@dataclass
class Transaction:
    id: str
    type: str
    date: str
    amount: int
    category: str
    memo: str
    tags: list[str]


@dataclass
class RecurringTransaction:
    id: str
    type: str
    day: int
    amount: int
    category: str
    memo: str
    tags: list[str]