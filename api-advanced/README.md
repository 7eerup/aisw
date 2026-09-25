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
