"""민감정보 마스킹과 diff 제한 기능의 단위 테스트."""

import pytest

from app.sanitizer import (
    limit_diff_lines,
    mask_sensitive_data,
    sanitize_diff,
)


def test_mask_email():
    """이메일 주소를 마스킹해야 한다."""
    text = "Contact: developer@example.com"

    result = mask_sensitive_data(text)

    assert "developer@example.com" not in result
    assert "[MASKED_EMAIL]" in result


def test_mask_prefixed_secret():
    """접두사가 있는 API Key를 마스킹해야 한다."""
    text = "Authorization: Bearer sk-example123456789"

    result = mask_sensitive_data(text)

    assert "sk-example123456789" not in result
    assert "[MASKED_SECRET]" in result


def test_mask_secret_assignment():
    """환경변수 형식의 민감정보를 마스킹해야 한다."""
    text = 'OPENAI_API_KEY="example-secret-value"'

    result = mask_sensitive_data(text)

    assert "example-secret-value" not in result
    assert "[MASKED_SECRET]" in result


def test_limit_long_diff():
    """긴 diff는 최대 200줄로 제한해야 한다."""
    diff_text = "\n".join(
        f"line {number}" for number in range(250)
    )

    result = limit_diff_lines(diff_text)

    assert len(result.splitlines()) == 200
    assert result.splitlines()[-1] == (
        "[TRUNCATED: 51 lines omitted]"
    )


def test_keep_short_diff():
    """200줄 이하의 diff는 그대로 반환해야 한다."""
    diff_text = "line 1\nline 2"

    result = limit_diff_lines(diff_text)

    assert result == diff_text


def test_invalid_max_lines():
    """최대 줄 수가 0 이하면 예외가 발생해야 한다."""
    with pytest.raises(
        ValueError,
        match="1 이상의 정수",
    ):
        limit_diff_lines("sample diff", max_lines=0)


def test_sanitize_diff():
    """마스킹과 줄 제한을 한 번에 적용해야 한다."""
    lines = ["developer@example.com"]
    lines.extend(
        f"line {number}" for number in range(250)
    )
    diff_text = "\n".join(lines)

    result = sanitize_diff(diff_text)

    assert "developer@example.com" not in result
    assert "[MASKED_EMAIL]" in result
    assert len(result.splitlines()) == 200
