import argparse
from pathlib import Path

from .decorators import handle_errors
from .repository import CategoryRepository, TransactionRepository
from .service import BudgetService
from .validators import is_valid_amount, is_valid_date, is_valid_type

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
    date_from: str | None = None,
    date_to: str | None = None,
    category: str | None = None,
    transaction_type: str | None = None,
    query: str | None = None,
    tag: str | None = None,
) -> None:
    """조건에 맞는 거래 내역을 최신순으로 출력한다."""

    if date_from is not None and not is_valid_date(date_from):
        raise ValueError("--from 날짜 형식이 올바르지 않습니다.")

    if date_to is not None and not is_valid_date(date_to):
        raise ValueError("--to 날짜 형식이 올바르지 않습니다.")

    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise ValueError("--from 날짜는 --to 날짜보다 늦을 수 없습니다.")

    transactions = service.search_transactions(
        date_from=date_from,
        date_to=date_to,
        category=category,
        transaction_type=transaction_type,
        query=query,
        tag=tag,
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
        print("검색 결과가 없습니다.")


@handle_errors
def main() -> int:
    """명령행 인자를 처리하고 가계부 기능을 실행한다."""
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
        "--from",
        dest="date_from",
        help="검색 시작 날짜(YYYY-MM-DD)",
    )

    search_parser.add_argument(
        "--to",
        dest="date_to",
        help="검색 종료 날짜(YYYY-MM-DD)",
    )

    search_parser.add_argument(
        "--category",
        help="카테고리로 검색합니다.",
    )

    search_parser.add_argument(
        "--type",
        dest="transaction_type",
        choices=["income", "expense"],
        help="거래 타입으로 검색합니다.",
    )

    search_parser.add_argument(
        "--q",
        dest="query",
        help="메모 키워드로 검색합니다.",
    )

    search_parser.add_argument(
        "--tag",
        help="태그로 검색합니다.",
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
            date_from=args.date_from,
            date_to=args.date_to,
            category=args.category,
            transaction_type=args.transaction_type,
            query=args.query,
            tag=args.tag,
        )

    return 0
