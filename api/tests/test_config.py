"""환경설정 모듈의 단위 테스트."""

import pytest

from app.config import ConfigurationError, get_api_key


def test_get_api_key(monkeypatch):
    """환경변수에 설정된 API Key를 반환해야 한다."""
    monkeypatch.setenv(
        "AI_API_KEY",
        "test-api-key",
    )

    result = get_api_key()

    assert result == "test-api-key"


def test_get_api_key_removes_whitespace(monkeypatch):
    """API Key 앞뒤의 공백을 제거해야 한다."""
    monkeypatch.setenv(
        "AI_API_KEY",
        "  test-api-key  ",
    )

    result = get_api_key()

    assert result == "test-api-key"


def test_missing_api_key(monkeypatch):
    """API Key가 없으면 설정 예외가 발생해야 한다."""
    monkeypatch.delenv(
        "AI_API_KEY",
        raising=False,
    )

    with pytest.raises(
        ConfigurationError,
        match="AI_API_KEY 환경변수가 설정되지 않았습니다",
    ):
        get_api_key()
