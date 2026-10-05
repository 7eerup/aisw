from collections import deque
from typing import Iterator

from .models import Transaction
from .repository import CategoryRepository, TransactionRepository
from .validators import is_valid_amount, is_valid_date, is_valid_type


class BudgetService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def category_exists(self, category: str) -> bool:
        """카테고리의 존재 여부를 반환한다."""
        return any(
            saved_category == category
            for saved_category in self.category_repository.get_all()
        )

    def _generate_id(self) -> str:
        """새로운 거래 ID를 생성한다."""
        max_number = 0

        for transaction in self.transaction_repository.get_all():
            number = int(transaction.id.split("-")[1])
            max_number = max(max_number, number)

        return f"TX-{max_number + 1:06d}"

    def add_transaction(
        self,
        date: str,
        transaction_type: str,
        amount: int,
        category: str,
        memo: str = "",
        tags: list[str] | None = None,
    ) -> Transaction:
        """입력값을 검증하고 거래 내역을 저장한다."""

        if not is_valid_date(date):
            raise ValueError("날짜 형식이 올바르지 않습니다.")

        if not is_valid_type(transaction_type):
            raise ValueError("거래 타입은 income 또는 expense여야 합니다.")

        if not is_valid_amount(amount):
            raise ValueError("금액은 0보다 커야 합니다.")

        if not self.category_exists(category):
            raise ValueError("등록되지 않은 카테고리입니다.")

        transaction = Transaction(
            id=self._generate_id(),
            type=transaction_type,
            date=date,
            amount=amount,
            category=category,
            memo=memo,
            tags=tags or [],
        )

        self.transaction_repository.add(transaction)

        return transaction

    def list_transactions(self) -> Iterator[Transaction]:
        """저장된 거래 내역을 한 건씩 반환한다."""
        yield from self.transaction_repository.get_all()

    def latest_transactions(
        self,
        transactions: Iterator[Transaction],
        limit: int,
    ) -> Iterator[Transaction]:
        """거래 내역 중 최신 N건을 최신순으로 반환한다."""
        latest = deque(transactions, maxlen=limit)

        while latest:
            yield latest.pop()

    def search_transactions(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        category: str | None = None,
        transaction_type: str | None = None,
        query: str | None = None,
        tag: str | None = None,
    ) -> Iterator[Transaction]:
        """조건에 맞는 거래 내역을 최신순으로 한 건씩 반환한다."""

        for transaction in self.transaction_repository.get_all_latest():
            if date_from is not None and transaction.date < date_from:
                continue

            if date_to is not None and transaction.date > date_to:
                continue

            if category is not None and transaction.category != category:
                continue

            if (
                transaction_type is not None
                and transaction.type != transaction_type
            ):
                continue

            if (
                query is not None
                and query.lower() not in transaction.memo.lower()
            ):
                continue

            if tag is not None and tag not in transaction.tags:
                continue

            yield transaction
