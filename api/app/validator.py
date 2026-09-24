"""AI가 생성한 커밋 메시지와 PR 초안을 검증하는 모듈."""


MAX_COMMIT_TITLE_LENGTH = 72
MAX_PR_TITLE_LENGTH = 80

REQUIRED_PR_SECTIONS = (
    "## Why",
    "## What",
    "## How to Test",
)


class OutputValidationError(ValueError):
    """AI 생성 결과가 필수 형식을 만족하지 않을 때 발생한다."""


def remove_code_fences(text: str) -> str:
    """AI 응답에서 Markdown 코드 블록 구분선을 제거한다."""
    lines = text.strip().splitlines()

    filtered_lines = [
        line
        for line in lines
        if not line.strip().startswith("```")
    ]

    return "\n".join(filtered_lines).strip()


def truncate_title(
    title: str,
    max_length: int,
) -> str:
    """제목을 최대 길이에 맞춰 줄인다."""
    if len(title) <= max_length:
        return title

    truncated_title = title[:max_length - 3].rstrip()
    return f"{truncated_title}..."


def validate_commit_message(text: str) -> str:
    """커밋 제목을 검증하고 최대 72자로 후처리한다."""
    cleaned_text = remove_code_fences(text)

    if not cleaned_text:
        raise OutputValidationError(
            "생성된 커밋 메시지가 비어 있습니다."
        )

    lines = cleaned_text.splitlines()
    title = lines[0].strip()

    if not title:
        raise OutputValidationError(
            "커밋 제목이 없습니다."
        )

    title = truncate_title(
        title,
        MAX_COMMIT_TITLE_LENGTH,
    )
    body = "\n".join(lines[1:]).strip()

    if body:
        return f"{title}\n\n{body}"

    return title


def find_section_lines(
    body_lines: list[str],
    section_header: str,
) -> list[str]:
    """지정한 PR 섹션에 포함된 내용을 반환한다."""
    section_start = None

    for index, line in enumerate(body_lines):
        if line.strip() == section_header:
            section_start = index + 1
            break

    if section_start is None:
        raise OutputValidationError(
            f"PR 본문에 {section_header} 섹션이 없습니다."
        )

    section_lines = []

    for line in body_lines[section_start:]:
        if line.strip().startswith("## "):
            break

        section_lines.append(line)

    return section_lines


def validate_pr_draft(text: str) -> str:
    """PR 제목과 필수 본문 구조를 검증한다."""
    cleaned_text = remove_code_fences(text)

    if not cleaned_text:
        raise OutputValidationError(
            "생성된 PR 초안이 비어 있습니다."
        )

    lines = cleaned_text.splitlines()
    title = lines[0].strip()

    if not title:
        raise OutputValidationError(
            "PR 제목이 없습니다."
        )

    title = truncate_title(
        title,
        MAX_PR_TITLE_LENGTH,
    )
    body_lines = lines[1:]

    for section_header in REQUIRED_PR_SECTIONS:
        section_lines = find_section_lines(
            body_lines,
            section_header,
        )

        has_bullet = any(
            line.strip().startswith("- ")
            for line in section_lines
        )

        if not has_bullet:
            raise OutputValidationError(
                f"{section_header} 섹션에 불릿이 없습니다."
            )

    body = "\n".join(body_lines).strip()
    return f"{title}\n\n{body}"


def validate_generated_text(
    command: str,
    generated_text: str,
) -> str:
    """CLI 명령에 맞는 결과 검증 함수를 실행한다."""
    if command == "commit":
        return validate_commit_message(generated_text)

    if command == "pr":
        return validate_pr_draft(generated_text)

    raise OutputValidationError(
        f"지원하지 않는 명령입니다: {command}"
    )
