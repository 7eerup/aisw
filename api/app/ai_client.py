"""OpenAI 호환 Chat Completions API 호출 모듈."""

import openai
from openai import OpenAI


DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 1


class AIClientError(RuntimeError):
    """AI API 요청 또는 응답 처리에 실패한 경우 발생하는 예외."""


def generate_text(
    api_key: str,
    base_url: str,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
) -> str:
    """OpenAI 호환 API를 호출해 생성된 텍스트를 반환한다."""
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        max_retries=DEFAULT_MAX_RETRIES,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except openai.AuthenticationError as error:
        raise AIClientError(
            "AI API 인증에 실패했습니다. "
            "virtual key를 확인하세요."
        ) from error
    except openai.RateLimitError as error:
        raise AIClientError(
            "AI API 요청 한도를 초과했습니다."
        ) from error
    except openai.APITimeoutError as error:
        raise AIClientError(
            "AI API 요청 시간이 초과되었습니다."
        ) from error
    except openai.APIConnectionError as error:
        raise AIClientError(
            "AI API 서버에 연결할 수 없습니다."
        ) from error
    except openai.APIStatusError as error:
        raise AIClientError(
            f"AI API 요청 실패: HTTP {error.status_code}"
        ) from error
    except openai.APIError as error:
        raise AIClientError(
            f"AI API 처리 중 오류가 발생했습니다: {error}"
        ) from error

    try:
        output_text = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError) as error:
        raise AIClientError(
            "AI API 응답 형식을 처리할 수 없습니다."
        ) from error

    if not output_text or not output_text.strip():
        raise AIClientError(
            "AI API가 비어 있는 응답을 반환했습니다."
        )

    return output_text.strip()
