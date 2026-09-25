"""명령행 인자와 옵션을 처리하는 모듈."""

import argparse

from app.sanitizer import MAX_DIFF_LINES

DEFAULT_MODEL = "gpt-5.4-mini"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 500
DEFAULT_CONVENTION = "default"
CONVENTION_CHOICES = (
    "default",
    "team",
)


def parse_temperature(value: str) -> float:
    """temperature 값을 검증하고 실수로 반환한다."""
    temperature = float(value)

    if not 0.0 <= temperature <= 2.0:
        raise argparse.ArgumentTypeError(
            "temperature는 0.0 이상 2.0 이하여야 합니다."
        )

    return temperature


def parse_max_tokens(value: str) -> int:
    """max_tokens 값을 검증하고 정수로 반환한다."""
    max_tokens = int(value)

    if max_tokens <= 0:
        raise argparse.ArgumentTypeError(
            "max-tokens는 1 이상의 정수여야 합니다."
        )

    return max_tokens


def parse_max_diff_lines(value: str) -> int:
    """diff 최대 줄 수를 검증하고 정수로 반환한다."""
    max_diff_lines = int(value)

    if max_diff_lines <= 0:
        raise argparse.ArgumentTypeError(
            "max-diff-lines는 1 이상의 정수여야 합니다."
        )

    return max_diff_lines


def add_common_options(parser: argparse.ArgumentParser) -> None:
    """commit과 pr 명령에서 사용할 공통 옵션을 추가한다."""
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"사용할 AI 모델 (기본값: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--temperature",
        type=parse_temperature,
        default=DEFAULT_TEMPERATURE,
        help="응답의 무작위성 설정 (기본값: 0.2)",
    )
    parser.add_argument(
        "--max-tokens",
        type=parse_max_tokens,
        default=DEFAULT_MAX_TOKENS,
        help="최대 출력 토큰 수 (기본값: 500)",
    )
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="민감정보 제거 및 diff 전송 범위 제한",
    )
    parser.add_argument(
        "--max-diff-lines",
        type=parse_max_diff_lines,
        default=MAX_DIFF_LINES,
        help=(
            "safe-mode에서 전송할 diff 최대 줄 수 "
            f"(기본값: {MAX_DIFF_LINES})"
        ),
    )
    parser.add_argument(
        "--convention",
        choices=CONVENTION_CHOICES,
        default=DEFAULT_CONVENTION,
        help=(
            "커밋/PR 컨벤션 선택 "
            f"(기본값: {DEFAULT_CONVENTION})"
        ),
    )


def build_parser() -> argparse.ArgumentParser:
    """프로그램에서 사용할 인자 파서를 생성한다."""
    parser = argparse.ArgumentParser(
        description="AI 기반 Git 커밋 및 PR 초안 생성기",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    commit_parser = subparsers.add_parser(
        "commit",
        help="커밋 메시지를 생성한다.",
    )
    add_common_options(commit_parser)

    pr_parser = subparsers.add_parser(
        "pr",
        help="PR 제목과 본문을 생성한다.",
    )
    add_common_options(pr_parser)

    return parser


def parse_arguments(
    arguments: list[str] | None = None,
) -> argparse.Namespace:
    """명령행 인자를 분석해 반환한다."""
    parser = build_parser()
    return parser.parse_args(arguments)
