"""AI 생성 결과 검증 모듈의 단위 테스트."""

import pytest

from app.validator import (
    OutputValidationError,
    validate_commit_message,
    validate_generated_text,
    validate_pr_draft,
)


VALID_PR_DRAFT = """feat: PR 자동 생성 기능 추가

## Why
- PR 작성 시간을 줄이기 위해 필요합니다.

## What
- PR 초안 생성 기능을 추가했습니다.

## How to Test
- python main.py pr 명령을 실행합니다.
"""


def test_validate_commit_message():
    """올바른 커밋 메시지는 그대로 반환해야 한다."""
    message = (
        "feat: 검증 기능 추가\n\n"
        "- app/validator.py 추가"
    )

    result = validate_commit_message(message)

    assert result == message


def test_truncate_commit_title():
    """72자를 초과한 커밋 제목은 줄여야 한다."""
    long_title = "feat: " + ("긴제목" * 30)

    result = validate_commit_message(long_title)
    title = result.splitlines()[0]

    assert len(title) <= 72
    assert title.endswith("...")


def test_reject_empty_commit_message():
    """빈 커밋 메시지는 거부해야 한다."""
    with pytest.raises(
        OutputValidationError,
        match="비어 있습니다",
    ):
        validate_commit_message("   ")


def test_validate_pr_draft():
    """필수 구조가 있는 PR 초안은 통과해야 한다."""
    result = validate_pr_draft(VALID_PR_DRAFT)

    assert result.strip() == VALID_PR_DRAFT.strip()


def test_truncate_pr_title():
    """80자를 초과한 PR 제목은 줄여야 한다."""
    long_title = "feat: " + ("긴제목" * 35)
    pr_draft = VALID_PR_DRAFT.replace(
        "feat: PR 자동 생성 기능 추가",
        long_title,
    )

    result = validate_pr_draft(pr_draft)
    title = result.splitlines()[0]

    assert len(title) <= 80
    assert title.endswith("...")


def test_reject_missing_pr_section():
    """필수 섹션이 빠진 PR 초안은 거부해야 한다."""
    invalid_draft = VALID_PR_DRAFT.replace(
        "## How to Test",
        "## Test",
    )

    with pytest.raises(
        OutputValidationError,
        match="How to Test",
    ):
        validate_pr_draft(invalid_draft)


def test_reject_section_without_bullet():
    """PR 섹션에 불릿이 없으면 거부해야 한다."""
    invalid_draft = VALID_PR_DRAFT.replace(
        "- PR 작성 시간을 줄이기 위해 필요합니다.",
        "PR 작성 시간을 줄이기 위해 필요합니다.",
    )

    with pytest.raises(
        OutputValidationError,
        match="불릿이 없습니다",
    ):
        validate_pr_draft(invalid_draft)


@pytest.mark.parametrize(
    ("command", "generated_text"),
    [
        (
            "commit",
            "feat: 커밋 메시지 검증 추가",
        ),
        (
            "pr",
            VALID_PR_DRAFT,
        ),
    ],
)
def test_validate_generated_text(
    command,
    generated_text,
):
    """CLI 명령에 맞는 결과 검증 함수를 선택해야 한다."""
    result = validate_generated_text(
        command,
        generated_text,
    )

    assert result
