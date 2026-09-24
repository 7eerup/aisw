"""Git diff의 민감정보와 전송 범위를 처리하는 모듈."""

import re


MAX_DIFF_LINES = 200

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PREFIXED_SECRET_PATTERN = re.compile(
    r"\b(?:sk|pk)-[A-Za-z0-9_-]{8,}\b",
    re.IGNORECASE,
)

SENSITIVE_ASSIGNMENT_PATTERN = re.compile(
    r"([\"']?[A-Z0-9_-]*"
    r"(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD)"
    r"[\"']?\s*[:=]\s*)"
    r"[\"']?([^\"',\s]+)[\"']?",
    re.IGNORECASE,
)


def mask_sensitive_data(text: str) -> str:
    """API Key, 토큰, 비밀번호 및 이메일을 마스킹한다."""
    masked_text = SENSITIVE_ASSIGNMENT_PATTERN.sub(
        r"\1[MASKED_SECRET]",
        text,
    )
    masked_text = PREFIXED_SECRET_PATTERN.sub(
        "[MASKED_SECRET]",
        masked_text,
    )
    masked_text = EMAIL_PATTERN.sub(
        "[MASKED_EMAIL]",
        masked_text,
    )

    return masked_text


def limit_diff_lines(
    diff_text: str,
    max_lines: int = MAX_DIFF_LINES,
) -> str:
    """diff를 지정된 최대 줄 수 이내로 제한한다."""
    if max_lines <= 0:
        raise ValueError("max_lines는 1 이상의 정수여야 합니다.")

    lines = diff_text.splitlines()

    if len(lines) <= max_lines:
        return diff_text

    retained_line_count = max_lines - 1
    omitted_line_count = len(lines) - retained_line_count

    limited_lines = lines[:retained_line_count]
    limited_lines.append(
        f"[TRUNCATED: {omitted_line_count} lines omitted]"
    )

    return "\n".join(limited_lines)


def sanitize_diff(
    diff_text: str,
    max_lines: int = MAX_DIFF_LINES,
) -> str:
    """diff의 민감정보를 제거하고 줄 수를 제한한다."""
    masked_diff = mask_sensitive_data(diff_text)
    return limit_diff_lines(masked_diff, max_lines)
