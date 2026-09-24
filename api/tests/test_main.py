"""메인 자동화 흐름의 단위 테스트."""

from argparse import Namespace
from unittest.mock import patch

import main as main_module

from app.config import ConfigurationError


def create_arguments(
    command: str = "commit",
    safe_mode: bool = False,
) -> Namespace:
    """테스트용 CLI 인자를 생성한다."""
    return Namespace(
        command=command,
        model="test-model",
        temperature=0.2,
        max_tokens=500,
        safe_mode=safe_mode,
    )


@patch("main.generate_text")
@patch("main.get_api_key")
@patch("main.collect_git_changes")
@patch("main.parse_arguments")
def test_main_generates_commit_message(
    mock_parse_arguments,
    mock_collect_git_changes,
    mock_get_api_key,
    mock_generate_text,
    capsys,
):
    """변경 사항이 있으면 커밋 메시지를 생성해야 한다."""
    mock_parse_arguments.return_value = create_arguments()
    mock_collect_git_changes.return_value = (
        "M app/main.py",
        "sample diff",
    )
    mock_get_api_key.return_value = "test-api-key"
    mock_generate_text.return_value = (
        "feat: 테스트 기능 추가\n\n"
        "- app/main.py 변경"
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "[DONE] AI 초안 생성 완료" in output
    assert "--- Commit Message ---" in output
    assert "feat: 테스트 기능 추가" in output
    mock_generate_text.assert_called_once()


@patch("main.generate_text")
@patch("main.get_api_key")
@patch("main.collect_git_changes")
@patch("main.parse_arguments")
def test_main_stops_without_changes(
    mock_parse_arguments,
    mock_collect_git_changes,
    mock_get_api_key,
    mock_generate_text,
    capsys,
):
    """변경 사항이 없으면 API를 호출하지 않아야 한다."""
    mock_parse_arguments.return_value = create_arguments()
    mock_collect_git_changes.return_value = ("", "")

    main_module.main()

    output = capsys.readouterr().out

    assert "변경 사항이 없습니다" in output
    mock_get_api_key.assert_not_called()
    mock_generate_text.assert_not_called()


@patch("main.generate_text")
@patch("main.get_api_key")
@patch("main.collect_git_changes")
@patch("main.parse_arguments")
def test_main_handles_missing_api_key(
    mock_parse_arguments,
    mock_collect_git_changes,
    mock_get_api_key,
    mock_generate_text,
    capsys,
):
    """API Key가 없으면 오류를 출력하고 종료해야 한다."""
    mock_parse_arguments.return_value = create_arguments()
    mock_collect_git_changes.return_value = (
        "M app/main.py",
        "sample diff",
    )
    mock_get_api_key.side_effect = ConfigurationError(
        "AI_API_KEY 환경변수가 설정되지 않았습니다."
    )

    main_module.main()

    output = capsys.readouterr().out

    assert "[ERROR]" in output
    assert "AI_API_KEY" in output
    mock_generate_text.assert_not_called()
