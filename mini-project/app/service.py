from collections import deque
from typing import Iterator

from .models import Transaction
from .repository import BudgetRepository, CategoryRepository, TransactionRepository
from .validators import is_valid_amount, is_valid_date, is_valid_type


class BudgetService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
        budget_repository: BudgetRepository,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.budget_repository = budget_repository

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

    def summarize_month(
        self,
        month: str,
        top: int = 3,
    ) -> dict:
        """월별 수입, 지출, 잔액과 카테고리별 지출을 집계한다."""
        total_income = 0
        total_expense = 0
        category_expenses: dict[str, int] = {}
        found = False

        for transaction in self.transaction_repository.get_all():
            if not transaction.date.startswith(f"{month}-"):
                continue

            found = True

            if transaction.type == "income":
                total_income += transaction.amount

            elif transaction.type == "expense":
                total_expense += transaction.amount
                category_expenses[transaction.category] = (
                    category_expenses.get(transaction.category, 0)
                    + transaction.amount
                )

        top_categories = sorted(
            category_expenses.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:top]

        budget = self.budget_repository.get_by_month(month)

        budget_amount = None
        budget_usage = None
        over_budget = False

        if budget is not None:
            budget_amount = budget["amount"]
            budget_usage = (total_expense / budget_amount) * 100
            over_budget = total_expense > budget_amount

        return {
            "found": found,
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense,
            "top_categories": top_categories,
            "budget": budget_amount,
            "budget_usage": budget_usage,
            "over_budget": over_budget,
        }

    def set_budget(
        self,
        month: str,
        amount: int,
    ) -> None:
        """지정한 월의 예산을 저장한다."""
        if amount <= 0:
            raise ValueError("예산은 0보다 커야 합니다.")

        self.budget_repository.set(
            month=month,
            amount=amount,
        )

    def add_category(self, name: str) -> None:
        """새로운 카테고리를 저장한다."""
        name = name.strip()

        if not name:
            raise ValueError("카테고리 이름은 비어 있을 수 없습니다.")

        if self.category_exists(name):
            raise ValueError("이미 등록된 카테고리입니다.")

        self.category_repository.add(name)

    def list_categories(self) -> Iterator[str]:
        """등록된 카테고리를 한 건씩 반환한다."""
        yield from self.category_repository.get_all()

    def category_in_use(self, name: str) -> bool:
        """카테고리가 거래 내역에서 사용 중인지 확인한다."""
        return any(
            transaction.category == name
            for transaction in self.transaction_repository.get_all()
        )

    def remove_category(self, name: str) -> None:
        """사용 중이지 않은 카테고리를 삭제한다."""
        if not self.category_exists(name):
            raise ValueError("등록되지 않은 카테고리입니다.")

        if self.category_in_use(name):
            raise ValueError(
                "거래 내역에서 사용 중인 카테고리는 삭제할 수 없습니다."
            )

        self.category_repository.remove(name)

    def update_transaction(
        self,
        transaction_id: str,
        date: str | None = None,
        transaction_type: str | None = None,
        amount: int | None = None,
        category: str | None = None,
        memo: str | None = None,
        tags: list[str] | None = None,
    ) -> Transaction:
        """지정한 거래의 입력된 필드만 수정한다."""
        transaction = self.transaction_repository.get_by_id(transaction_id)

        if transaction is None:
            raise ValueError("해당 ID의 거래 내역이 없습니다.")

        if date is not None:
            if not is_valid_date(date):
                raise ValueError("날짜 형식이 올바르지 않습니다.")
            transaction.date = date

        if transaction_type is not None:
            if not is_valid_type(transaction_type):
                raise ValueError(
                    "거래 타입은 income 또는 expense여야 합니다."
                )
            transaction.type = transaction_type

        if amount is not None:
            if not is_valid_amount(amount):
                raise ValueError("금액은 0보다 커야 합니다.")
            transaction.amount = amount

        if category is not None:
            if not self.category_exists(category):
                raise ValueError("등록되지 않은 카테고리입니다.")
            transaction.category = category

        if memo is not None:
            transaction.memo = memo

        if tags is not None:
            transaction.tags = tags

        self.transaction_repository.update(transaction)

        return transaction

    def delete_transaction(self, transaction_id: str) -> None:
        """지정한 ID의 거래를 삭제한다."""
        deleted = self.transaction_repository.delete(transaction_id)

        if not deleted:
            raise ValueError("해당 ID의 거래 내역이 없습니다.")