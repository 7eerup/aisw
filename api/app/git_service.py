"""Git 명령을 실행하고 변경 사항을 수집하는 모듈."""

import subprocess


class GitCommandError(RuntimeError):
    """Git 명령 실행에 실패했을 때 발생하는 예외."""


def run_git_command(*arguments: str) -> str:
    """Git 명령을 실행하고 표준 출력을 반환한다."""
    command = ["git", *arguments]

    result = subprocess.run(
        command,
        capture_output=True,
        check=False,
        text=True,
    )

    if result.returncode != 0:
        error_message = result.stderr.strip() or "Git 명령 실행 실패"
        raise GitCommandError(error_message)

    return result.stdout.strip()


def validate_git_repository() -> None:
    """현재 디렉토리가 Git 저장소인지 확인한다."""
    result = run_git_command(
        "rev-parse",
        "--is-inside-work-tree",
    )

    if result != "true":
        raise GitCommandError("현재 디렉토리는 Git 저장소가 아닙니다.")


def get_git_status() -> str:
    """현재 디렉토리의 변경 파일 목록을 반환한다."""
    return run_git_command(
        "status",
        "--short",
        "--untracked-files=all",
        "--",
        ".",
    )


def get_git_diff() -> str:
    """현재 디렉토리의 스테이징 전후 변경 내용을 반환한다."""
    unstaged_diff = run_git_command(
        "diff",
        "--",
        ".",
    )
    staged_diff = run_git_command(
        "diff",
        "--cached",
        "--",
        ".",
    )

    diff_sections = []

    if unstaged_diff:
        diff_sections.append(
            "[Unstaged Changes]\n"
            f"{unstaged_diff}"
        )

    if staged_diff:
        diff_sections.append(
            "[Staged Changes]\n"
            f"{staged_diff}"
        )

    return "\n\n".join(diff_sections)


def collect_git_changes() -> tuple[str, str]:
    """Git 상태와 diff 내용을 함께 수집한다."""
    validate_git_repository()

    status = get_git_status()
    diff = get_git_diff()

    return status, diff
