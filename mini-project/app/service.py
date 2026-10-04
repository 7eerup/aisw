from typing import Iterator

from .models import Transaction
from .repository import TransactionRepository, CategoryRepository
from .validators import is_valid_date, is_valid_type, is_valid_amount


class BudgetService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
    ):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository

    def category_exists(self, category: str) -> bool:
        return any(
            saved_category == category
            for saved_category in self.category_repository.get_all()
        )

    def _generate_id(self) -> str:
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

    def list_transactions(
        self,
        transaction_type: str | None = None,
        category: str | None = None,
        tag: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        min_amount: int | None = None,
        max_amount: int | None = None,
    ) -> Iterator[Transaction]:
        """조건에 맞는 거래 내역을 한 건씩 반환한다."""
        for transaction in self.transaction_repository.get_all():
            if (
                transaction_type is not None
                and transaction.type != transaction_type
            ):
                continue

            if (
                category is not None
                and transaction.category != category
            ):
                continue

            if (
                tag is not None
                and tag not in transaction.tags
            ):
                continue

            if (
                date_from is not None
                and transaction.date < date_from
            ):
                continue

            if (
                date_to is not None
                and transaction.date > date_to
            ):
                continue

            if (
                min_amount is not None
                and transaction.amount < min_amount
            ):
                continue

            if (
                max_amount is not None
                and transaction.amount > max_amount
            ):
                continue

            yield transaction
