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

    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    transaction = service.add_transaction(
        date=date,
        transaction_type=transaction_type,
        amount=amount,
        category=category,
        memo=memo,
        tags=tags,
    )

    print(f"[저장 완료] id={transaction.id}")


def handle_list(
    service: BudgetService,
    limit: int = 10,
) -> None:
    """저장된 거래 내역을 최신순으로 출력한다."""

    if limit < 1:
        raise ValueError("--limit은 1 이상이어야 합니다.")

    transactions = service.list_transactions()

    transactions = service.latest_transactions(
        transactions,
        limit,
    )

    found = False

    for transaction in transactions:
        found = True

        print(
            f"{transaction.id} | "
            f"{transaction.date} | "
            f"{transaction.type} | "
            f"{transaction.category} | "
            f"{transaction.amount} | "
            f"{transaction.memo} | "
            f"{', '.join(transaction.tags)}"
        )

    if not found:
        print("거래 내역이 없습니다.")


def handle_search(
    service: BudgetService,
    keyword: str,
) -> None:
    """검색어와 일치하는 거래 내역을 출력한다."""
    found = False

    for transaction in service.search_transactions(keyword):
        found = True

        print(
            f"{transaction.id} | "
            f"{transaction.date} | "
            f"{transaction.type} | "
            f"{transaction.category} | "
            f"{transaction.amount} | "
            f"{transaction.memo} | "
            f"{', '.join(transaction.tags)}"
        )

    if not found:
        print("검색 결과가 없습니다.")


@handle_errors
def main() -> int:
    parser = argparse.ArgumentParser(description="파일 기반 가계부 프로그램")

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "add",
        help="거래를 추가합니다.",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="거래 내역을 조회합니다.",
    )

    list_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="출력할 최대 거래 수 (기본값: 10)",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="거래 내역을 검색합니다.",
    )

    search_parser.add_argument(
        "keyword",
        help="메모 또는 태그에서 검색할 키워드",
    )

    args = parser.parse_args()

    transaction_repository = TransactionRepository(DATA_DIR / "transactions.jsonl")
    category_repository = CategoryRepository(DATA_DIR / "categories.jsonl")

    service = BudgetService(
        transaction_repository,
        category_repository,
    )

    if args.command == "add":
        handle_add(service)

    elif args.command == "list":
        handle_list(
            service,
            limit=args.limit,
        )

    elif args.command == "search":
        handle_search(
            service,
            keyword=args.keyword,
        )

    return 0
