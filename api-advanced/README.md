# 실제 리포지토리 적용 및 PR 완성

AI 기반 Git 커밋 및 PR 생성기를 이전 미션인 Mini Redis 프로젝트에 적용

## 적용 결과

* 적용 프로젝트: `mini-redis`
* 작업 브랜치: `docs/improve-usage-guide`
* 변경 내용: Mini Redis 실행 환경, 실행 방법, 종료 방법 및 빠른 검증 명령 추가
* 커밋: `4504b0b docs(docs): Mini Redis 실행 및 환경 안내 추가`
* PR: [#4 docs(docs): Mini Redis 실행 및 환경 안내 추가](https://github.com/7eerup/aisw/pull/4)
* 병합 상태: Main 브랜치 병합 완료

## AI 생성 결과

AI가 생성한 커밋 메시지 초안은 다음과 같습니다.

```text
docs(cli): 실행 방법과 환경 안내 추가

- README.md에 Python 3.10 이상 실행 환경과 외부 패키지 불필요 사항을 정리함
- mini-redis 실행 예시, 종료 방법, 표준 입력 기반 빠른 확인 절차를 README.md에 추가함
```

AI가 생성한 PR 제목은 다음과 같습니다.

```text
docs(readme): 실행 방법과 환경 안내 추가
```

## AI 초안에서 최종 PR로 변경한 내용

1. AI 커밋 제목의 `docs(cli)`를 문서 변경에 더 적합한 `docs(docs)`로 수정했습니다.
2. AI PR 제목의 `readme`는 팀 컨벤션에서 허용한 scope가 아니므로 `docs`로 교정했습니다.
3. 제목에 `Mini Redis`를 추가해 변경 대상을 명확하게 표현했습니다.
4. 변경 파일을 일반적인 `README.md` 대신 `mini-redis/README.md`로 구체화했습니다.
5. 실제 검증에 사용한 표준 입력 실행 명령을 `How to Test`에 반영했습니다.
6. 예상 출력 결과를 추가해 검토자가 정상 동작 여부를 확인할 수 있도록 보완했습니다.


# 커밋 및 PR 템플릿 커스터마이징

선택한 이전 미션인 Mini Redis가 포함된 저장소의 기존 커밋 스타일을 분석하고 팀 컨벤션을 정의했습니다. CLI 옵션을 통해 기본 컨벤션과 팀 컨벤션을 선택할 수 있도록 구현했습니다.

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

## 구현 방식

* `app/cli.py`에 `--convention {default,team}` 옵션을 추가했습니다.
* `app/prompt_builder.py`에서 선택한 컨벤션에 따라 추가 규칙을 프롬프트에 적용합니다.
* `main.py`에서 선택한 컨벤션을 프롬프트 생성 과정에 전달합니다.

## 사용 방법

기본 컨벤션:

```bash
python main.py commit --convention default
```

팀 컨벤션:

```bash
python main.py commit --convention team
```

PR 초안에도 같은 옵션을 사용할 수 있습니다.

```bash
python main.py pr --convention team
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

- CLI에 --convention 옵션을 추가해 커밋과 PR 컨벤션을 선택할 수 있도록 했습니다.
- prompt_builder.py와 main.py에서 선택된 컨벤션에 따라 프롬프트를 구성하도록 반영했습니다.
```

팀 컨벤션을 적용하면 커밋 제목에 `cli` scope가 추가되어 변경 범위를 제목에서 바로 확인할 수 있습니다.

실제 Mini Redis 문서 변경에는 다음 팀 컨벤션을 적용했습니다.

```text
4504b0b docs(docs): Mini Redis 실행 및 환경 안내 추가
```



# Safe-mode 고도화


## safe-mode 정책과 숫자 기준

* safe-mode OFF에서는 마스킹과 diff 줄 제한을 적용하지 않습니다.
* safe-mode ON에서는 민감정보를 마스킹하고 diff를 기본 최대 200줄로 제한합니다.
* `--max-diff-lines`에는 1 이상의 정수를 지정할 수 있으며, 초과한 내용은 생략된 줄 수로 표시합니다.



## safe-mode ON/OFF 비교

다음 명령은 실제 API를 호출하지 않고 safe-mode 적용 전후를 비교합니다. 테스트 데이터는 실제 API Key가 아닌 더미 값입니다.

```bash
python -c '
from pathlib import Path
from app.sanitizer import sanitize_diff

source = Path("config.txt").read_text(
    encoding="utf-8",
)

print("--- safe-mode OFF ---")
print(source)

print("--- safe-mode ON: 최대 3줄 ---")
print(sanitize_diff(source, max_lines=3))
'
```

### safe-mode OFF

```text
--- safe-mode OFF ---
EMAIL=user@example.com
API_KEY=sk-example123456789
SERVICE_NAME=sample-app
ENVIRONMENT=development
DEBUG=false
```

### safe-mode ON 및 최대 3줄 생략

```text
--- safe-mode ON: 최대 3줄 ---
EMAIL=[MASKED_EMAIL]
API_KEY=[MASKED_SECRET]
[TRUNCATED: 3 lines omitted]
```
