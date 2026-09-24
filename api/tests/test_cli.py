"""CLI 명령과 옵션에 대한 단위 테스트."""

import pytest

from app.cli import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    parse_arguments,
)


def test_commit_command_defaults():
    """commit 명령에 기본 옵션이 적용되어야 한다."""
    arguments = parse_arguments(["commit"])

    assert arguments.command == "commit"
    assert arguments.model == DEFAULT_MODEL
    assert arguments.temperature == DEFAULT_TEMPERATURE
    assert arguments.max_tokens == DEFAULT_MAX_TOKENS
    assert arguments.safe_mode is False


def test_pr_command_with_safe_mode():
    """pr 명령에서 safe-mode를 활성화할 수 있어야 한다."""
    arguments = parse_arguments(["pr", "--safe-mode"])

    assert arguments.command == "pr"
    assert arguments.safe_mode is True


def test_custom_options():
    """사용자가 지정한 API 옵션이 반영되어야 한다."""
    arguments = parse_arguments(
        [
            "commit",
            "--model",
            "test-model",
            "--temperature",
            "0.3",
            "--max-tokens",
            "700",
        ]
    )

    assert arguments.model == "test-model"
    assert arguments.temperature == 0.3
    assert arguments.max_tokens == 700


def test_invalid_temperature():
    """허용 범위를 벗어난 temperature는 거부해야 한다."""
    with pytest.raises(SystemExit):
        parse_arguments(
            [
                "commit",
                "--temperature",
                "2.1",
            ]
        )


def test_invalid_max_tokens():
    """0 이하의 max-tokens는 거부해야 한다."""
    with pytest.raises(SystemExit):
        parse_arguments(
            [
                "pr",
                "--max-tokens",
                "0",
            ]
        )
