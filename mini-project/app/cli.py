import argparse
from pathlib import Path

from .repository import TransactionRepository, CategoryRepository
from .service import BudgetService
from .decorators import handle_errors
from .validators import is_valid_date, is_valid_type, is_valid_amount


DATA_DIR = Path("data")


def handle_add(service: BudgetService) -> None:
    """대화형으로 거래 정보를 입력받아 저장한다."""

    while True:
        date = input("날짜(YYYY-MM-DD): ")

        if is_valid_date(date):
            break

        print("[오류] 날짜 형식이 올바르지 않습니다.")
        print("[힌트] YYYY-MM-DD 형식으로 입력하세요.")

    while True:
        transaction_type = input("타입(income/expense): ")

        if is_valid_type(transaction_type):
            break

        print("[오류] income 또는 expense를 입력하세요.")

    while True:
        category = input("카테고리: ")

        if service.category_exists(category):
            break

        print("[오류] 등록되지 않은 카테고리입니다.")

    while True:
        try:
            amount = int(input("금액(양수): "))

            if is_valid_amount(amount):
                break

            print("[오류] 금액은 0보다 커야 합니다.")

        except ValueError:
            print("[오류] 금액은 숫자로 입력해야 합니다.")

    memo = input("메모(선택): ")
    tags_input = input("태그(쉼표로 구분, 없으면 엔터): ")

    tags = [
        tag.strip()
        for tag in tags_input.split(",")
        if tag.strip()
    ]

    transaction = service.add_transaction(
        date=date,
        transaction_type=transaction_type,
        amount=amount,
        category=category,
        memo=memo,
        tags=tags,
    )

    print(f"[저장 완료] id={transaction.id}")


@handle_errors
def main() -> None:
    parser = argparse.ArgumentParser(
        description="파일 기반 가계부 프로그램"
    )

    parser.add_argument(
        "command",
        choices=["add"],
        help="실행할 명령",
    )

    args = parser.parse_args()

    transaction_repository = TransactionRepository(
        DATA_DIR / "transactions.jsonl"
    )
    category_repository = CategoryRepository(
        DATA_DIR / "categories.jsonl"
    )

    service = BudgetService(
        transaction_repository,
        category_repository,
    )

    if args.command == "add":
        handle_add(service)
