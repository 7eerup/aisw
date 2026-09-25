# 커밋 및 PR 템플릿 커스터마이징

기존 커밋 스타일을 분석하고 팀 컨벤션을 정의한 뒤, CLI 옵션으로 기본 컨벤션과 팀 컨벤션을 선택할 수 있도록 구현했습니다.

## 기존 스타일 분석

기존 커밋에서는 `feat`, `fix`, `docs`, `refactor`, `chore` 등의 prefix를 사용했지만, 변경 범위를 나타내는 scope는 일관되게 사용하지 않았습니다.

변경 모듈을 제목에서 바로 확인할 수 있도록 팀 컨벤션에서는 `type(scope)` 형식을 사용합니다.

## 팀 컨벤션

### 제목 형식

```text
type(scope): 한국어 요약
```

### 허용 type

| type       | 용도                |
| ---------- | ----------------- |
| `feat`     | 새로운 기능 추가         |
| `fix`      | 오류 수정             |
| `docs`     | 문서 변경             |
| `refactor` | 기능 변화 없는 코드 구조 개선 |
| `chore`    | 설정 및 기타 작업        |

### 허용 scope

| scope    | 대상                |
| -------- | ----------------- |
| `cli`    | CLI 명령과 옵션        |
| `api`    | AI API 연동         |
| `git`    | Git 명령 및 변경 사항 수집 |
| `prompt` | 프롬프트 생성           |
| `safe`   | 민감정보 및 diff 제한    |
| `docs`   | README와 문서        |

### 커밋 본문

* 제목 다음에 빈 줄을 추가합니다.
* 핵심 변경 사항을 1~2개 불릿으로 작성합니다.
* 변경된 파일이나 모듈을 1~3개 언급합니다.

### PR 형식

* PR 제목에도 `type(scope): 한국어 요약` 형식을 적용합니다.
* `## Why`, `## What`, `## How to Test` 구조를 유지합니다.
* `## What`에는 변경된 파일이나 모듈을 언급합니다.
* `## How to Test`에는 실제 실행 가능한 명령을 작성합니다.

## 사용 방법

기본 컨벤션:

```bash
python main.py commit \
  --safe-mode \
  --max-diff-lines 50 \
  --convention default
```

팀 컨벤션:

```bash
python main.py commit \
  --safe-mode \
  --max-diff-lines 50 \
  --convention team
```

PR 초안에도 같은 옵션을 사용할 수 있습니다.

```bash
python main.py pr \
  --safe-mode \
  --max-diff-lines 50 \
  --convention team
```

## 적용 전후 비교

### 기본 컨벤션

```text
feat: 커밋 컨벤션 선택 옵션 추가

- app/cli.py에 --convention 옵션과 기본 컨벤션 값을 추가해 출력 형식을 선택할 수 있게 했습니다.
- app/prompt_builder.py와 main.py에서 선택된 컨벤션에 따라 커밋 메시지 프롬프트를 구성하도록 반영했습니다.
```

### 팀 컨벤션

```text
feat(cli): 커밋 컨벤션 선택 옵션 추가

- CLI에 --convention 옵션을 추가해 커밋/PR 컨벤션을 선택할 수 있도록 했습니다.
- prompt_builder와 main에서 선택된 컨벤션에 따라 프롬프트를 구성하도록 반영했습니다.
```

팀 컨벤션을 적용하면 커밋 제목에 `cli` scope가 추가되어 변경 범위를 제목에서 바로 확인할 수 있습니다.


# Safe-mode 고도화

safe-mode에서 AI API로 전송할 Git diff의 최대 줄 수를 사용자가 직접 설정할 수 있도록 기능을 확장했습니다.

## 구현 내용

* `--max-diff-lines` CLI 옵션 추가
* 기본 diff 제한값 200줄 적용
* 1 이상의 정수만 입력 가능
* 이메일, API Key, 토큰, 비밀번호 마스킹
* 사용자 지정 줄 수를 safe-mode 처리 과정에 적용
* 적용된 diff 제한값을 실행 로그에 출력

## 실행 방법

```bash
python main.py commit \
  --model gpt-5.4-mini \
  --temperature 0.2 \
  --max-tokens 500 \
  --safe-mode \
  --max-diff-lines 50
```

추가된 옵션:

* `--max-diff-lines`: safe-mode에서 전송할 diff 최대 줄 수(기본값: 200)

## 적용 정책

| 설정                    | 민감정보 마스킹                   | diff 줄 제한              |
| --------------------- | -------------------------- | ---------------------- |
| safe-mode OFF         | 적용하지 않음                    | 적용하지 않음                |
| safe-mode ON          | 이메일, API Key, 토큰, 비밀번호 마스킹 | 기본 최대 200줄             |
| safe-mode ON + 사용자 지정 | 이메일, API Key, 토큰, 비밀번호 마스킹 | `--max-diff-lines`로 지정 |

`--max-diff-lines`에는 1 이상의 정수만 입력할 수 있습니다. `0` 이하의 값은 CLI 입력 검증 단계에서 거부됩니다.

## 기본 200줄 제한

```bash
python main.py commit --safe-mode
```

```text
[INFO] safe-mode 적용: 민감정보 마스킹 및 diff 200줄 제한
```

## 사용자 지정 50줄 제한

```bash
python main.py commit \
  --safe-mode \
  --max-diff-lines 50
```

```text
[INFO] safe-mode 적용: 민감정보 마스킹 및 diff 50줄 제한
```

## 실제 API 실행 결과

```text
[INFO] safe-mode 적용: 민감정보 마스킹 및 diff 50줄 제한
[INFO] 실행 명령: commit
[INFO] AI 모델: gpt-5.4-mini
[INFO] AI API Base URL: https://copa.codyssey.kr/v1
[INFO] AI API 요청 중...
[INFO] 출력 형식 검증 완료
[DONE] AI 초안 생성 완료

--- Commit Message ---
feat: safe-mode diff 줄 수 제한 옵션 추가

- app/cli.py에 --max-diff-lines 옵션과 검증 로직을 추가해 safe-mode 전송 범위를 제어하도록 개선
- main.py에서 새 옵션을 반영해 diff 처리 흐름과 기본 제한값을 연동하도록 수정
----------------------
```

## safe-mode ON/OFF 비교

입력 예시:

```text
EMAIL=user@example.com
API_KEY=sk-example123456789
line 3
line 4
line 5
```

safe-mode OFF:

```text
EMAIL=user@example.com
API_KEY=sk-example123456789
line 3
line 4
line 5
```

safe-mode ON 및 최대 3줄 제한:

```text
EMAIL=[MASKED_EMAIL]
API_KEY=[MASKED_SECRET]
[TRUNCATED: 3 lines omitted]
```

safe-mode를 적용하면 이메일과 API Key가 마스킹됩니다. 설정된 최대 줄 수를 초과한 내용은 생략되고, 마지막 줄에 생략된 줄 수가 표시됩니다.
