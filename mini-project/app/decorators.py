from functools import wraps
from typing import Callable


def handle_errors(func: Callable) -> Callable:
    """CLI 실행 중 발생한 오류를 사용자 친화적으로 출력한다."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except FileNotFoundError as error:
            print(f"[오류] 파일을 찾을 수 없습니다: {error.filename}")
            print("[힌트] 파일 경로와 파일명을 확인하세요.")
            return 1

        except ValueError as error:
            print(f"[오류] {error}")
            print("[힌트] 입력값을 확인한 후 다시 실행하세요.")
            return 1

    return wrapper
