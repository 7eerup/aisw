"""AI API 클라이언트의 단위 테스트."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import openai
import pytest

from app.ai_client import AIClientError, generate_text


def create_response(content: str):
    """테스트용 Chat Completions 응답을 생성한다."""
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=content,
                )
            )
        ]
    )


@patch("app.ai_client.OpenAI")
def test_generate_text(mock_openai):
    """AI 응답의 메시지 내용을 반환해야 한다."""
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value = (
        create_response("generated message")
    )

    result = generate_text(
        api_key="test-virtual-key",
        base_url="https://example.com/v1",
        prompt="sample prompt",
        model="test-model",
        temperature=0.2,
        max_tokens=500,
    )

    assert result == "generated message"

    mock_openai.assert_called_once_with(
        api_key="test-virtual-key",
        base_url="https://example.com/v1",
        timeout=30.0,
        max_retries=1,
    )

    mock_client.chat.completions.create.assert_called_once_with(
        model="test-model",
        messages=[
            {
                "role": "user",
                "content": "sample prompt",
            }
        ],
        temperature=0.2,
        max_tokens=500,
    )


@patch("app.ai_client.OpenAI")
def test_empty_response(mock_openai):
    """빈 AI 응답이 반환되면 예외가 발생해야 한다."""
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.return_value = (
        create_response("   ")
    )

    with pytest.raises(
        AIClientError,
        match="비어 있는 응답",
    ):
        generate_text(
            api_key="test-virtual-key",
            base_url="https://example.com/v1",
            prompt="sample prompt",
            model="test-model",
            temperature=0.2,
            max_tokens=500,
        )


@patch("app.ai_client.OpenAI")
def test_connection_error(mock_openai):
    """서버 연결 실패를 사용자용 예외로 변환해야 한다."""
    mock_client = mock_openai.return_value
    mock_client.chat.completions.create.side_effect = (
        openai.APIConnectionError(
            request=MagicMock(),
        )
    )

    with pytest.raises(
        AIClientError,
        match="서버에 연결할 수 없습니다",
    ):
        generate_text(
            api_key="test-virtual-key",
            base_url="https://example.com/v1",
            prompt="sample prompt",
            model="test-model",
            temperature=0.2,
            max_tokens=500,
        )
