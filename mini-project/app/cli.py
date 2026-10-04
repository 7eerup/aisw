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
    transaction_type: str | None = None,
    category: str | None = None,
    tag: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    min_amount: int | None = None,
    max_amount: int | None = None,
    page: int = 1,
    page_size: int = 10,
    sort: str = "id",
    order: str = "asc",
) -> None:
    """저장된 거래 내역을 출력한다."""

    # 날짜 검증
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

    # 금액 검증
    if min_amount is not None and min_amount < 0:
        raise ValueError("--min 금액은 0 이상이어야 합니다.")

    if max_amount is not None and max_amount < 0:
        raise ValueError("--max 금액은 0 이상이어야 합니다.")

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise ValueError("--min 금액은 --max 금액보다 클 수 없습니다.")

    # 페이지 검증
    if page < 1:
        raise ValueError("--page는 1 이상이어야 합니다.")

    if page_size < 1:
        raise ValueError("--page-size는 1 이상이어야 합니다.")

    # 필터링
    transactions = service.list_transactions(
        transaction_type,
        category,
        tag,
        date_from,
        date_to,
        min_amount,
        max_amount,
    )

    transactions = service.sort_transactions(
        transactions,
        sort,
        order,
    )

    # 페이지네이션
    transactions = service.paginate_transactions(
        transactions,
        page,
        page_size,
    )

    # 출력
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
        print("조건에 맞는 거래 내역이 없습니다.")


@handle_errors
def main() -> None:
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
        "--type",
        choices=["income", "expense"],
        help="거래 타입으로 필터링합니다.",
    )

    list_parser.add_argument(
        "--category",
        help="카테고리로 필터링합니다.",
    )

    list_parser.add_argument(
        "--tag",
        help="태그로 필터링합니다.",
    )

    list_parser.add_argument(
        "--from",
        dest="date_from",
        help="조회 시작 날짜(YYYY-MM-DD)",
    )

    list_parser.add_argument(
        "--to",
        dest="date_to",
        help="조회 종료 날짜(YYYY-MM-DD)",
    )

    list_parser.add_argument(
        "--min",
        dest="min_amount",
        type=int,
        help="최소 금액",
    )

    list_parser.add_argument(
        "--max",
        dest="max_amount",
        type=int,
        help="최대 금액",
    )

    list_parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="페이지 번호 (기본값: 1)",
    )

    list_parser.add_argument(
        "--page-size",
        type=int,
        default=10,
        help="페이지당 거래 수 (기본값: 10)",
    )

    list_parser.add_argument(
        "--sort",
        choices=["id"],
        default="id",
        help="정렬 기준 (기본값: id)",
    )

    list_parser.add_argument(
        "--order",
        choices=["asc"],
        default="asc",
        help="정렬 방향 (기본값: asc)",
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
            transaction_type=args.type,
            category=args.category,
            tag=args.tag,
            date_from=args.date_from,
            date_to=args.date_to,
            min_amount=args.min_amount,
            max_amount=args.max_amount,
            page=args.page,
            page_size=args.page_size,
            sort=args.sort,
            order=args.order,
        )
