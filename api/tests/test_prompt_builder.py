"""프롬프트 생성 모듈의 단위 테스트."""

import pytest

from app.prompt_builder import (
    build_commit_prompt,
    build_pr_prompt,
    build_prompt,
)


SAMPLE_STATUS = "M app/main.py"
SAMPLE_DIFF = "diff --git a/app/main.py b/app/main.py"


def test_build_commit_prompt():
    """커밋 프롬프트에 Git 정보와 규칙이 포함되어야 한다."""
    prompt = build_commit_prompt(
        SAMPLE_STATUS,
        SAMPLE_DIFF,
    )

    assert SAMPLE_STATUS in prompt
    assert SAMPLE_DIFF in prompt
    assert "최대 72자" in prompt
    assert "1~2개 불릿" in prompt
    assert "커밋 메시지만 출력" in prompt


def test_build_pr_prompt():
    """PR 프롬프트에 필수 섹션과 Git 정보가 포함되어야 한다."""
    prompt = build_pr_prompt(
        SAMPLE_STATUS,
        SAMPLE_DIFF,
    )

    assert SAMPLE_STATUS in prompt
    assert SAMPLE_DIFF in prompt
    assert "최대 80자" in prompt
    assert "## Why" in prompt
    assert "## What" in prompt
    assert "## How to Test" in prompt


def test_build_commit_prompt_without_diff():
    """diff가 없으면 대체 문구가 포함되어야 한다."""
    prompt = build_commit_prompt(
        SAMPLE_STATUS,
        "",
    )

    assert "(diff 내용 없음)" in prompt


@pytest.mark.parametrize(
    ("command", "expected_text"),
    [
        ("commit", "Git 커밋 메시지"),
        ("pr", "Pull Request 초안"),
    ],
)
def test_build_prompt_routes_command(
    command,
    expected_text,
):
    """CLI 명령에 맞는 프롬프트를 선택해야 한다."""
    prompt = build_prompt(
        command,
        SAMPLE_STATUS,
        SAMPLE_DIFF,
    )

    assert expected_text in prompt


def test_build_prompt_rejects_unknown_command():
    """지원하지 않는 명령은 거부해야 한다."""
    with pytest.raises(
        ValueError,
        match="지원하지 않는 명령",
    ):
        build_prompt(
            "unknown",
            SAMPLE_STATUS,
            SAMPLE_DIFF,
        )
