```
사용자
 │
 │ python -m app add
 ▼
┌────────────────────────┐
│ app/__main__.py        │
│ main() 실행             │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ cli.py                 │
│ argparse → add 확인     │
│ Repository 생성         │
│ Service 생성            │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ handle_add()           │
│ input()                │
└───────────┬────────────┘
            │
            ├── 날짜 ───────▶ validators.py
            │                 is_valid_date()
            │
            ├── type ───────▶ validators.py
            │                 is_valid_type()
            │
            ├── category ───▶ service.py
            │                 category_exists()
            │                       ↓
            │                 CategoryRepository
            │                       ↓
            │                 categories.jsonl
            │
            └── amount ─────▶ validators.py
                              is_valid_amount()

            ▼
┌────────────────────────┐
│ service.py             │
│ add_transaction()      │
│ 거래 추가 업무 처리     │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ models.py              │
│ Transaction 객체       │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ repository.py          │
│ TransactionRepository │
│ add()                  │
└───────────┬────────────┘
            ▼
┌────────────────────────┐
│ transactions.jsonl     │
│ JSON 한 줄 추가         │
└───────────┬────────────┘
            ▼
         service
            ↓
       handle_add()
            ↓
[저장 완료] id=TX-000001



__main__.py
→ 프로그램 시작

cli.py
→ 명령 분석 + 사용자 입력/출력

validators.py
→ 입력값 검증

service.py
→ 거래 추가 업무 로직

models.py
→ Transaction 데이터 구조

repository.py
→ JSONL 파일 읽기/쓰기

decorators.py
→ 공통 예외 처리

transactions.jsonl
→ 실제 거래 데이터 영구 저장
```