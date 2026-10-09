# 파일 기반 가계부 콘솔 프로그램

Python 표준 라이브러리 활용한 파일 기반 가계부 CLI 프로그램

거래 내역, 카테고리, 월별 예산을 JSONL 파일로 관리하며 검색, 수정, 삭제, CSV 가져오기/내보내기, 반복 거래, 백업 기능을 제공합니다.


## 프로젝트 구조

```text
.
├── README.md
├── app
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── decorators.py
│   ├── models.py
│   ├── repository.py
│   ├── service.py
│   └── validators.py
└── data
    ├── transactions.jsonl
    ├── categories.jsonl
    ├── budgets.jsonl
    └── recurring.jsonl
```

## 표준 라이브러리

| 표준 라이브러리 | 사용 목적 |
|---|---|
| `argparse` | `add`, `list`, `search` 같은 CLI 명령어와 옵션 처리 |
| `pathlib` | 데이터 파일과 디렉터리 경로 처리 |
| `datetime` | 백업 파일의 타임스탬프 생성 |
| `shutil` | JSONL 데이터 파일 백업 |
| `unicodedata` | 한글의 터미널 출력 너비를 계산해 테이블 정렬 |
| `collections` | `deque`를 사용해 최신 N건 거래 처리 |
| `typing` | `Iterator`, `Callable` 등 타입 힌트 작성 |
| `dataclasses` | `Transaction`, `RecurringTransaction` 데이터 모델 정의 |
| `json` | JSONL 형식의 거래·카테고리·예산·반복 내역 저장/읽기 |
| `csv` | 거래 내역 CSV import/export |
| `functools` | `wraps`를 이용한 오류 처리 데코레이터 구현 |
| `sys` | 프로그램 종료 코드(`sys.exit`) 처리 |


## 파일/모듈 역할

- `cli.py` → 사용자 명령 입력, 옵션 처리, 결과 출력
- `service.py` → 거래 검증, 검색, 요약, 예산, 반복 거래 등 핵심 로직 처리
- `repository.py` → JSONL/CSV 파일 읽기, 저장, 수정, 삭제
- `models.py` → Transaction, RecurringTransaction 데이터 구조 정의
- `validators.py` → 날짜, 금액, 타입, 월 형식 검증
- `decorators.py` → 공통 예외 처리 및 오류 메시지 출력
- `__main__.py` → python -m app 실행 진입점


## 실행 방법

```bash
python -m app --help
```

기본 데이터 저장 위치 `./data`

다른 데이터 폴더를 사용하려면 `--data-dir` 옵션을 지정합니다.

```bash
python -m app --data-dir custom_data list
```

데이터 파일이 없으면 실행 시 자동으로 생성됩니다.


## 데이터 저장 구조

기본적으로 다음 JSONL 파일을 사용합니다.

```text
data/
├── transactions.jsonl
├── categories.jsonl
├── budgets.jsonl
├── recurring.jsonl
└── backups/
```

## 거래 데이터

- `id`: 고유 거래 ID
- `type`: `income` 또는 `expense`
- `date`: `YYYY-MM-DD`
- `amount`: 0보다 큰 정수
- `category`: 등록된 카테고리
- `memo`: 선택 입력
- `tags`: 선택 입력


## 주요 기능

- 거래 추가
- 최신 거래 목록 조회
- 조건별 거래 검색
- 월별 수입·지출·잔액 요약
- 월별 예산 설정 및 사용률 확인
- 카테고리 추가·조회·삭제
- 거래 수정·삭제
- CSV 가져오기·내보내기
- 반복 거래 등록 및 월별 적용
- 데이터 파일 백업
- 한글을 고려한 콘솔 테이블 정렬
- 수정·삭제 시 임시 파일을 이용한 안전한 파일 교체

## 실행

### 거래 추가

```bash
python -m app add
```


```bash
python -m app category add --name food
```

### 거래 목록

```bash
python -m app list
python -m app list --limit 5
```

### 거래 조건 검색(type, date, category memo, tag)

```bash
python -m app search --type expense
python -m app search --category food
python -m app search --from 2026-10-01 --to 2026-10-31
python -m app search --q coffee
python -m app search --tag drink
```

조건은 함께 사용할 수 있습니다.

### 월별 요약

```bash
python -m app summary --month 2026-10
python -m app summary --month 2026-10 --top 5
```

다음 정보를 확인할 수 있습니다.

- 총수입
- 총지출
- 잔액
- 카테고리별 지출 TOP N
- 예산
- 예산 사용률
- 예산 초과 여부

### 예산 설정

```bash
python -m app budget set --month 2026-10 --amount 1000000
```

### 카테고리 관리

```bash
python -m app category add --name food
python -m app category list
python -m app category remove --name food
```

거래 내역에서 사용 중인 카테고리는 삭제할 수 없습니다.

### 거래 수정

거래 수정은 옵션 방식으로 구현했습니다.

```bash
python -m app update --id TX-000001 --amount 15000
```

여러 항목을 동시에 수정할 수도 있습니다.

```bash
python -m app update --id TX-000001 --date 2026-10-06 --category food --memo "점심"
```

### 거래 삭제

```bash
python -m app delete --id TX-000001
```

존재하지 않는 ID를 입력하면 오류 메시지와 함께 비정상 종료 코드가 반환됩니다.

## CSV 가져오기

```bash
python -m app import --from transactions.csv
```

## CSV 내보내기

월 단위:

```bash
python -m app export --out october.csv --month 2026-10
```

기간 단위:

```bash
python -m app export \
  --out range.csv \
  --from 2026-10-01 \
  --to 2026-10-31
```


## advanced

- 타임스탬프 기반 데이터 백업
- 반복 거래 등록 및 특정 월 자동 생성
- 한글을 고려한 콘솔 테이블 정렬
- 임시 파일 작성 후 교체하는 안전한 수정·삭제 방식


### 데이터 백업

데이터 파일 `backups` 디렉터리에 타임스탬프가 포함된 이름으로 백업합니다.

```bash
python -m app backup
```


```bash
find data/backups -type f
```


## 반복 거래

월급, 월세 등 반복되는 거래를 등록하고 특정 월의 실제 거래로 생성할 수 있습니다.

### 반복 거래 등록

```bash
python -m app recurring add --day 25 --type income --amount 3000000 --category salary
```

반복 날짜는 `1~28` 범위로 제한합니다.

### 반복 거래 조회

```bash
python -m app recurring list
```

### 특정 월에 적용

```bash
python -m app recurring apply --month 2026-10
```

등록된 반복 거래가 해당 월의 실제 거래 내역으로 생성됩니다.

## 출력 정렬

거래 목록과 검색 결과는 한글 너비를 고려한 고정 너비 형식으로 출력하며, 금액은 오른쪽 정렬합니다.

```bash
python -m app list --limit 5
python -m app search --type income
python -m app recurring list
```


## 파일 저장 안정성

거래 수정과 삭제 시 임시 파일에 변경 내용을 먼저 작성한 뒤 기존 파일을 교체합니다.

수정 테스트:

```bash
python -m app update --id TX-000001 --amount 15000
```

삭제 테스트:

```bash
python -m app delete --id TX-000001
```

정상 처리 후 임시 파일이 남아 있지 않은지 확인할 수 있습니다.

```bash
find data -maxdepth 1 -name "*.tmp" -print
```

출력이 없으면 임시 파일 교체가 정상적으로 완료된 상태입니다.
