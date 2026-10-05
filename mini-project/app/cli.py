import argparse
from pathlib import Path

from .decorators import handle_errors
from .repository import BudgetRepository, CategoryRepository, TransactionRepository
from .service import BudgetService
from .validators import is_valid_amount, is_valid_date, is_valid_month, is_valid_type

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


def handle_summary(
    service: BudgetService,
    month: str,
    top: int = 3,
) -> None:
    """월별 거래 요약과 예산 사용 현황을 집계한다."""

    if not is_valid_month(month):
        raise ValueError("--month 형식은 YYYY-MM이어야 합니다.")

    if top < 1:
        raise ValueError("--top은 1 이상이어야 합니다.")

    summary = service.summarize_month(
        month=month,
        top=top,
    )

    if not summary["found"]:
        print(f"{month} 거래 내역이 없습니다.")
        return

    print(f"총수입: {summary['income']}")
    print(f"총지출: {summary['expense']}")
    print(f"잔액: {summary['balance']}")

    if summary["budget"] is not None:
        print(f"예산: {summary['budget']}")
        print(f"예산 사용률: {summary['budget_usage']:.1f}%")

        if summary["over_budget"]:
            print("[경고] 예산을 초과했습니다.")

    print("\n카테고리별 지출 TOP")

    for category, amount in summary["top_categories"]:
        print(f"{category}: {amount}")


def handle_budget_set(
    service: BudgetService,
    month: str,
    amount: int,
) -> None:
    """월별 예산을 설정한다."""

    if not is_valid_month(month):
        raise ValueError("--month 형식은 YYYY-MM이어야 합니다.")

    if amount <= 0:
        raise ValueError("--amount는 0보다 커야 합니다.")

    service.set_budget(
        month=month,
        amount=amount,
    )

    print(f"[예산 설정 완료] {month}: {amount}")


def handle_category_add(
    service: BudgetService,
    name: str,
) -> None:
    """카테고리를 추가한다."""
    service.add_category(name)
    print(f"[카테고리 추가 완료] {name}")


def handle_category_list(service: BudgetService) -> None:
    """등록된 카테고리 목록을 출력한다."""
    found = False

    for category in service.list_categories():
        found = True
        print(category)

    if not found:
        print("등록된 카테고리가 없습니다.")


def handle_category_remove(
    service: BudgetService,
    name: str,
) -> None:
    """카테고리를 삭제한다."""
    service.remove_category(name)
    print(f"[카테고리 삭제 완료] {name}")


def handle_update(
    service: BudgetService,
    transaction_id: str,
    date: str | None = None,
    transaction_type: str | None = None,
    amount: int | None = None,
    category: str | None = None,
    memo: str | None = None,
    tags: str | None = None,
) -> None:
    """지정한 거래의 입력된 필드만 수정한다."""
    parsed_tags = None

    if tags is not None:
        parsed_tags = [
            tag.strip()
            for tag in tags.split(",")
            if tag.strip()
        ]

    transaction = service.update_transaction(
        transaction_id=transaction_id,
        date=date,
        transaction_type=transaction_type,
        amount=amount,
        category=category,
        memo=memo,
        tags=parsed_tags,
    )

    print(f"[수정 완료] id={transaction.id}")


def handle_delete(
    service: BudgetService,
    transaction_id: str,
) -> None:
    """지정한 거래를 삭제한다."""
    service.delete_transaction(transaction_id)
    print(f"[삭제 완료] id={transaction_id}")


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

    summary_parser = subparsers.add_parser(
        "summary",
        help="월별 거래 요약을 조회합니다.",
    )

    summary_parser.add_argument(
        "--month",
        required=True,
        help="조회할 연월(YYYY-MM)",
    )

    summary_parser.add_argument(
        "--top",
        type=int,
        default=3,
        help="출력할 지출 카테고리 수 (기본값: 3)",
    )

    budget_parser = subparsers.add_parser(
        "budget",
        help="월별 예산을 관리합니다.",
    )

    budget_subparsers = budget_parser.add_subparsers(
        dest="budget_command",
        required=True,
    )

    budget_set_parser = budget_subparsers.add_parser(
        "set",
        help="월별 예산을 설정합니다.",
    )

    budget_set_parser.add_argument(
        "--month",
        required=True,
        help="예산을 설정할 연월(YYYY-MM)",
    )

    budget_set_parser.add_argument(
        "--amount",
        type=int,
        required=True,
        help="예산 금액",
    )

    category_parser = subparsers.add_parser(
        "category",
        help="카테고리를 관리합니다.",
)

    category_subparsers = category_parser.add_subparsers(
        dest="category_command",
        required=True,
    )

    category_add_parser = category_subparsers.add_parser(
        "add",
        help="카테고리를 추가합니다.",
    )
    category_add_parser.add_argument(
        "--name",
        required=True,
        help="추가할 카테고리 이름",
    )

    category_subparsers.add_parser(
        "list",
        help="카테고리 목록을 조회합니다.",
    )

    category_remove_parser = category_subparsers.add_parser(
        "remove",
        help="카테고리를 삭제합니다.",
    )
    category_remove_parser.add_argument(
        "--name",
        required=True,
        help="삭제할 카테고리 이름",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="거래 내역을 수정합니다.",
    )

    update_parser.add_argument(
        "--id",
        dest="transaction_id",
        required=True,
        help="수정할 거래 ID",
    )

    update_parser.add_argument(
        "--date",
        help="수정할 날짜(YYYY-MM-DD)",
    )

    update_parser.add_argument(
        "--type",
        dest="transaction_type",
        choices=["income", "expense"],
        help="수정할 거래 타입",
    )

    update_parser.add_argument(
        "--amount",
        type=int,
        help="수정할 금액",
    )

    update_parser.add_argument(
        "--category",
        help="수정할 카테고리",
    )

    update_parser.add_argument(
        "--memo",
        help="수정할 메모",
    )

    update_parser.add_argument(
        "--tags",
        help="수정할 태그(쉼표로 구분)",
    )


    delete_parser = subparsers.add_parser(
        "delete",
        help="거래 내역을 삭제합니다.",
    )

    delete_parser.add_argument(
        "--id",
        dest="transaction_id",
        required=True,
        help="삭제할 거래 ID",
    )

    args = parser.parse_args()

    transaction_repository = TransactionRepository(DATA_DIR / "transactions.jsonl")
    category_repository = CategoryRepository(DATA_DIR / "categories.jsonl")
    budget_repository = BudgetRepository(DATA_DIR / "budgets.jsonl")

    service = BudgetService(
        transaction_repository,
        category_repository,
        budget_repository,
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

    elif args.command == "summary":
        handle_summary(
            service,
            month=args.month,
            top=args.top,
        )

    elif args.command == "budget":
        if args.budget_command == "set":
            handle_budget_set(
                service,
                month=args.month,
                amount=args.amount,
            )

    elif args.command == "category":
        if args.category_command == "add":
            handle_category_add(
                service,
                name=args.name,
            )

        elif args.category_command == "list":
            handle_category_list(service)

        elif args.category_command == "remove":
            handle_category_remove(
                service,
                name=args.name,
            )

    elif args.command == "update":
        handle_update(
            service,
            transaction_id=args.transaction_id,
            date=args.date,
            transaction_type=args.transaction_type,
            amount=args.amount,
            category=args.category,
            memo=args.memo,
            tags=args.tags,
        )

    elif args.command == "delete":
        handle_delete(
            service,
            transaction_id=args.transaction_id,
        )

    return 0
