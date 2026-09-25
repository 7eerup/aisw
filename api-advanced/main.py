"""AI 기반 Git 커밋 및 PR 생성기 실행 모듈."""

from app.ai_client import AIClientError, generate_text
from app.cli import parse_arguments
from app.config import (
    ConfigurationError,
    get_ai_base_url,
    get_api_key,
)
from app.git_service import GitCommandError, collect_git_changes
from app.prompt_builder import build_prompt
from app.sanitizer import mask_sensitive_data, sanitize_diff
from app.validator import (
    OutputValidationError,
    validate_generated_text,
)


def print_generated_result(
    command: str,
    generated_text: str,
) -> None:
    """생성된 커밋 또는 PR 초안을 구분해서 출력한다."""
    if command == "commit":
        header = "Commit Message"
    else:
        header = "PR Draft"

    print(f"\n--- {header} ---")
    print(generated_text)
    print("----------------------")


def main() -> None:
    """Git 변경 내용을 기반으로 커밋 또는 PR 초안을 생성한다."""
    arguments = parse_arguments()

    try:
        status, diff = collect_git_changes()
    except GitCommandError as error:
        print(f"[ERROR] Git 명령 실행 실패: {error}")
        return

    if not status:
        print(
            "[INFO] 변경 사항이 없습니다. "
            "생성 작업을 종료합니다."
        )
        return

    if arguments.safe_mode:
        status = mask_sensitive_data(status)
        diff = sanitize_diff(diff)

        print(
            "[INFO] safe-mode 적용: "
            "민감정보 마스킹 및 diff 200줄 제한"
        )

    try:
        api_key = get_api_key()
        base_url = get_ai_base_url()
    except ConfigurationError as error:
        print(f"[ERROR] {error}")
        print(
            '예: export AI_API_KEY="YOUR_API_KEY"'
        )
        return

    prompt = build_prompt(
        arguments.command,
        status,
        diff,
    )

    print(f"[INFO] 실행 명령: {arguments.command}")
    print(f"[INFO] AI 모델: {arguments.model}")
    print(f"[INFO] AI API Base URL: {base_url}")
    print("[INFO] AI API 요청 중...")

    try:
        generated_text = generate_text(
            api_key=api_key,
            base_url=base_url,
            prompt=prompt,
            model=arguments.model,
            temperature=arguments.temperature,
            max_tokens=arguments.max_tokens,
        )
    except AIClientError as error:
        print(f"[ERROR] {error}")
        return

    try:
        validated_text = validate_generated_text(
            arguments.command,
            generated_text,
        )
    except OutputValidationError as error:
        print(
            f"[ERROR] AI 출력 형식 검증 실패: {error}"
        )
        return

    print("[INFO] 출력 형식 검증 완료")
    print("[DONE] AI 초안 생성 완료")

    print_generated_result(
        arguments.command,
        validated_text,
    )


if __name__ == "__main__":
    main()
