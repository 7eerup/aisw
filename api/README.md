# AI Git Commit & PR Generator

Git 변경 사항을 분석해 AI 기반 커밋 메시지와 Pull Request 초안을 생성하는 Python CLI 도구

`git status`와 `git diff` 결과를 OpenAI 호환 API에 전달하고, 생성 결과를 검증한 후 터미널에 출력합니다. 실제 Git 커밋이나 GitHub PR 생성은 수행하지 않습니다.

## 주요 기능

* Git 변경 파일 목록 수집
* staged 및 unstaged diff 수집
* AI 기반 커밋 메시지 생성
* AI 기반 PR 제목 및 본문 생성
* 모델, temperature, max_tokens 옵션 설정
* API 인증·연결·응답 오류 처리
* 커밋 및 PR 출력 형식 검증
* safe-mode를 통한 민감정보 마스킹
* safe-mode 사용 시 diff 최대 200줄 제한

## 개발 환경

* Python 3.10 이상
* Git
* OpenAI 호환 Chat Completions API

## 프로젝트 구조

```text
api/
├── app/
│   ├── __init__.py
│   ├── ai_client.py
│   ├── cli.py
│   ├── config.py
│   ├── git_service.py
│   ├── prompt_builder.py
│   ├── sanitizer.py
│   └── validator.py
├── tests/
│   ├── __init__.py
│   ├── test_ai_client.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_git_service.py
│   ├── test_main.py
│   ├── test_prompt_builder.py
│   ├── test_sanitizer.py
│   └── test_validator.py
├── main.py
├── README.md
└── requirements.txt
```

## 설치 방법

가상환경 생성 활성화 및 의존성 설치

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## 환경변수 설정

Copa에서 발급받은 virtual key를 `AI_API_KEY` 환경변수로 설정합니다.

```bash
export AI_API_KEY="YOUR_VIRTUAL_KEY"
```

기본 AI API Base URL은 다음과 같습니다.

```text
https://copa.codyssey.kr/v1
```

다른 OpenAI 호환 API를 사용하려면 `AI_BASE_URL` 환경변수를 설정할 수 있습니다.

```bash
export AI_BASE_URL="https://copa.codyssey.kr/v1"
```

`AI_BASE_URL`을 설정하지 않으면 프로그램에 정의된 기본 Base URL을 사용합니다.

API Key 설정 여부를 확인할 때는 전체 값을 출력하지 않습니다.

```bash
python -c '
import os

key = os.getenv("AI_API_KEY", "")
print("설정 여부:", bool(key))
print("문자 수:", len(key))
'
```

## 사용 방법

Git 저장소 내부의 분석할 프로젝트 디렉터리에서 명령을 실행합니다.

### 커밋 메시지 생성

```bash
python main.py commit
```

safe-mode를 적용하려면 다음과 같이 실행합니다.

```bash
python main.py commit --safe-mode
```

### PR 초안 생성

```bash
python main.py pr
```

safe-mode를 적용하려면 다음과 같이 실행합니다.

```bash
python main.py pr --safe-mode
```

### AI 파라미터 변경

```bash
python main.py commit \
  --model gpt-5.4-mini \
  --temperature 0.2 \
  --max-tokens 500 \
  --safe-mode
```

지원 옵션:

* `--model`: API 요청에 사용할 AI 모델
* `--temperature`: 생성 결과의 무작위성
* `--max-tokens`: 최대 출력 토큰 수
* `--safe-mode`: 민감정보 마스킹 및 diff 200줄 제한

사용 가능한 모델은 연결된 API 제공자의 지원 범위에 따라 달라질 수 있습니다.

## 커밋 메시지 출력 예시

```text
[INFO] safe-mode 적용: 민감정보 마스킹 및 diff 200줄 제한
[INFO] 실행 명령: commit
[INFO] AI 모델: gpt-5.4-mini
[INFO] AI API Base URL: https://copa.codyssey.kr/v1
[INFO] AI API 요청 중...
[INFO] 출력 형식 검증 완료
[DONE] AI 초안 생성 완료

--- Commit Message ---
feat: AI 기반 Git 메시지 생성기 초기 구현

- Git 변경 사항을 수집해 AI 입력으로 전달하는 기능을 구현함
- 커밋 및 PR 출력 형식 검증과 테스트를 추가함
----------------------
```

## PR 초안 출력 예시

```text
[INFO] safe-mode 적용: 민감정보 마스킹 및 diff 200줄 제한
[INFO] 실행 명령: pr
[INFO] AI 모델: gpt-5.4-mini
[INFO] AI API Base URL: https://copa.codyssey.kr/v1
[INFO] AI API 요청 중...
[INFO] 출력 형식 검증 완료
[DONE] AI 초안 생성 완료

--- PR Draft ---
feat: AI 기반 Git 커밋 및 PR 초안 생성기 추가

## Why
- 커밋 메시지와 PR 설명을 일관된 형식으로 작성하기 위해 필요합니다.

## What
- Git status와 diff 수집 기능을 구현했습니다.
- AI 기반 커밋 메시지 및 PR 초안 생성 기능을 추가했습니다.
- safe-mode와 출력 형식 검증 기능을 추가했습니다.

## How to Test
- `python -m pytest -v`로 전체 테스트를 실행합니다.
- `python main.py commit --safe-mode`를 실행합니다.
- `python main.py pr --safe-mode`를 실행합니다.
----------------------
```

AI가 생성하는 실제 문구는 입력된 Git 변경 사항과 모델에 따라 달라질 수 있습니다.

## 테스트

전체 단위 테스트를 실행합니다.

```bash
python -m pytest -v
```

Git 서비스 테스트만 실행하려면 다음 명령을 사용합니다.

```bash
python -m pytest tests/test_git_service.py -v
```

PEP 8 검사를 실행합니다.

```bash
pycodestyle main.py app tests
```

`pycodestyle` 실행 결과가 출력되지 않으면 검사를 통과한 것입니다.

## 안전 및 주의사항

* API Key를 소스 코드나 README에 직접 작성하지 않습니다.
* `.env`, 가상환경, `__pycache__`, `.pytest_cache`는 Git에 포함하지 않습니다.
* safe-mode는 이메일과 API Key 형태의 민감정보를 마스킹합니다.
* safe-mode는 API로 전달하는 diff를 최대 200줄로 제한합니다.
* 민감한 파일이 포함된 경우 API 요청 전에 diff를 직접 확인합니다.
* commit/pr 명령은 실행할 때마다 AI API를 한 번 호출하므로 사용량과 비용이 발생할 수 있습니다.
* 생성된 커밋 메시지와 PR 초안은 사용자가 검토한 후 적용해야 합니다.
* 프로그램은 `git commit`, `git push`, GitHub PR 생성을 자동으로 실행하지 않습니다.
