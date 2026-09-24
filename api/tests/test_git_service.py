"""Git 서비스 모듈의 단위 테스트."""

import subprocess
from unittest.mock import call, patch

import pytest

from app.git_service import (
    GitCommandError,
    collect_git_changes,
    get_git_diff,
    get_git_status,
    run_git_command,
    validate_git_repository,
)


@patch("app.git_service.run_git_command")
def test_get_git_status(mock_run_git_command):
    """현재 디렉토리의 untracked 파일까지 반환해야 한다."""
    mock_run_git_command.return_value = "?? main.py"

    result = get_git_status()

    mock_run_git_command.assert_called_once_with(
        "status",
        "--short",
        "--untracked-files=all",
        "--",
        ".",
    )
    assert result == "?? main.py"


@patch("app.git_service.subprocess.run")
def test_run_git_command_success(mock_run):
    """Git 명령 성공 시 표준 출력을 반환해야 한다."""
    mock_run.return_value = subprocess.CompletedProcess(
        args=["git", "status", "--short"],
        returncode=0,
        stdout=" M main.py\n",
        stderr="",
    )

    result = run_git_command("status", "--short")

    assert result == "M main.py"


@patch("app.git_service.subprocess.run")
def test_run_git_command_failure(mock_run):
    """Git 명령 실패 시 GitCommandError가 발생해야 한다."""
    mock_run.return_value = subprocess.CompletedProcess(
        args=["git", "status"],
        returncode=128,
        stdout="",
        stderr="fatal: not a git repository",
    )

    with pytest.raises(
        GitCommandError,
        match="not a git repository",
    ):
        run_git_command("status")


@patch("app.git_service.run_git_command")
def test_validate_git_repository_failure(mock_run_git_command):
    """Git 저장소가 아니면 예외가 발생해야 한다."""
    mock_run_git_command.return_value = "false"

    with pytest.raises(
        GitCommandError,
        match="Git 저장소가 아닙니다",
    ):
        validate_git_repository()


@patch("app.git_service.run_git_command")
def test_get_git_diff(mock_run_git_command):
    """스테이징 전후의 diff를 함께 반환해야 한다."""
    mock_run_git_command.side_effect = [
        "unstaged diff",
        "staged diff",
    ]

    result = get_git_diff()

    assert "[Unstaged Changes]" in result
    assert "unstaged diff" in result
    assert "[Staged Changes]" in result
    assert "staged diff" in result
    assert mock_run_git_command.call_args_list == [
        call("diff", "--", "."),
        call("diff", "--cached", "--", "."),
    ]


@patch("app.git_service.get_git_diff")
@patch("app.git_service.get_git_status")
@patch("app.git_service.validate_git_repository")
def test_collect_git_changes(
    mock_validate_repository,
    mock_get_status,
    mock_get_diff,
):
    """Git 상태와 diff를 함께 수집해야 한다."""
    mock_get_status.return_value = "M main.py"
    mock_get_diff.return_value = "sample diff"

    status, diff = collect_git_changes()

    mock_validate_repository.assert_called_once()
    assert status == "M main.py"
    assert diff == "sample diff"
