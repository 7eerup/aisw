"""AI API 실행에 필요한 환경설정을 관리하는 모듈."""

import os


API_KEY_ENV_NAME = "AI_API_KEY"
AI_BASE_URL_ENV_NAME = "AI_BASE_URL"

DEFAULT_AI_BASE_URL = "https://copa.codyssey.kr/v1"


class ConfigurationError(RuntimeError):
    """필수 환경설정이 없거나 잘못된 경우 발생하는 예외."""


def get_api_key() -> str:
    """환경변수에서 AI API Key를 읽어 반환한다."""
    api_key = os.getenv(API_KEY_ENV_NAME, "").strip()

    if not api_key:
        raise ConfigurationError(
            f"{API_KEY_ENV_NAME} 환경변수가 설정되지 않았습니다."
        )

    return api_key


def get_ai_base_url() -> str:
    """환경변수 또는 기본값에서 AI API 주소를 반환한다."""
    base_url = os.getenv(
        AI_BASE_URL_ENV_NAME,
        DEFAULT_AI_BASE_URL,
    ).strip()

    return base_url.rstrip("/")
