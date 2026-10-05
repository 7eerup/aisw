from datetime import datetime


def is_valid_date(value: str) -> bool:
    """YYYY-MM-DD 형식의 유효한 날짜인지 확인한다."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_type(value: str) -> bool:
    """거래 타입이 income 또는 expense인지 확인한다."""
    return value in ("income", "expense")


def is_valid_amount(value: int) -> bool:
    """금액이 양수인지 확인한다."""
    return value > 0


def is_valid_month(value: str) -> bool:
    """YYYY-MM 형식의 유효한 연월인지 확인한다."""
    try:
        datetime.strptime(value, "%Y-%m")
        return True
    except ValueError:
        return False