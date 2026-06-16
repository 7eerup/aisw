# FastAPI CRUD Memo Service

* FastAPI와 SQLAlchemy를 활용하여 구현한 메모 관리 웹 서비스
* CRUD = 소프트웨어와 데이터베이스에서 데이터를 처리하는 4가지 기본 기능인 생성(Create), 읽기(Read), 수정(Update), 삭제(Delete)

---

##
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "fastapi[standards]" sqlalchemy
fastapi dev
```

## 학습 내용

* FastAPI Router 사용
* Jinja2 기반 SSR
* SQLAlchemy ORM CRUD
* SQLite 연동
* Dependency Injection(Depends)
* Repository Pattern
* Service Layer 분리
* PRG(Post-Redirect-Get) 패턴 적용

---

## 주요 기능

### 홈 화면

* 서비스 소개
* 메모 목록 이동
* 새 메모 작성 이동

### 메모 CRUD

* 메모 목록 조회
* 메모 상세 조회
* 메모 등록
* 메모 수정
* 메모 삭제

### PRG(Post-Redirect-Get) 패턴

* 등록 후 Redirect
* 수정 후 Redirect
* 삭제 후 Redirect

새로고침(F5) 시 중복 요청이 발생하지 않도록 PRG(Post-Redirect-Get) 구현

---

## 프로젝트 구조

```text
fastapi-crud/
│
├── main.py
├── database.py
├── requirements.txt
│
├── models/
│   └── memo.py
│
├── repositories/
│   └── memo_repository.py
│
├── services/
│   └── memo_service.py
│
├── routers/
│   └── memo_router.py
│
└── templates/
    ├── home.html
    ├── memo_list.html
    ├── memo_detail.html
    ├── memo_form.html
    └── memo_not_found.html
```

---

## FastAPI 실행 구조
```
uvicorn main:app --reload
          │
          ▼
     FastAPI
          │
 ┌────────┼────────┐
 │        │        │
 ▼        ▼        ▼
 /      /docs   /redoc
 │        │        │
 ▼        ▼        ▼
홈화면  Swagger  ReDoc
```

## 기능 구현

| 기능       | URL                       | 방식                  |
| -------- | ------------------------- | ------------------- |
| 홈 화면     | `/`                       | GET                 |
| 메모 목록    | `/memos`                  | GET                 |
| 메모 상세    | `/memos/{memo_id}`        | GET                 |
| 메모 등록 화면 | `/memos/new`              | GET                 |
| 메모 등록 처리 | `/memos`                  | POST + Redirect 303 |
| 메모 수정 화면 | `/memos/{memo_id}/edit`   | GET                 |
| 메모 수정 처리 | `/memos/{memo_id}/edit`   | POST + Redirect 303 |
| 메모 삭제    | `/memos/{memo_id}/delete` | POST + Redirect 303 |


---

## CRUD 화면 흐름

```text
홈
 ├─ 메모 목록
 │   ├─ 상세 조회
 │   │   ├─ 수정
 │   │   └─ 삭제
 │   └─ 새 메모 작성
 └─ 새 메모 작성
```

---

## 브라우저 요청 FastAPI 서버에서 "라우터 → 서비스 → 저장소 → 템플릿" 흐름
* 사용자가 /memos에 접속하면 Router가 요청을 받고 DB Session을 생성한 뒤 Service에 전달
* Service는 Repository를 통해 SQLAlchemy ORM으로 SQLite를 조회하고, 조회 결과를 다시 Router로 반환
* Router는 Jinja2 Template에 데이터를 전달하여 HTML을 생성하고 브라우저에 응답

```
사용자 클릭
      │
      ▼
GET /memos
      │
      ▼
Router
(요청 URL 확인)
      │
      ▼
DB Session 생성
(SQLite와 통신할 준비)
      │
      ▼
Service
(비즈니스 로직 처리)
      │
      ▼
Repository
(DB 접근 담당)
      │
      ▼
SQLAlchemy ORM
(Python 객체 ↔ DB 테이블 매핑)
      │
      ▼
SQLite DB
(memos 테이블 조회)
      │
      ▲
      │
Repository
      │
      ▲
      │
Service
      │
      ▲
      │
Router
      │
      ▼
Jinja2 Template
(HTML 렌더링)
      │
      ▼
HTML 생성
      │
      ▼
브라우저 출력
(200 OK)
```

* http://127.0.0.1:8000/memos
* FastAPI가 URL을 확인 - router.get("/memos") 실행
* DB Session 생성 - FastAPI가 SQLite와 통신하기 위해 DB 연결(Session) 과정
* DB Session 생성 -> Router 전달 -> 작업 완료 -> 자동 close()
* Service 호출 - Router가 받은 요청을 Service에게 "목록 요청" 이라고 넘기는 과정
* Service 처리 = Repository 호출
* Service 따로 두는 이유는 Router Service Repository 역할 섞임 방지
* Repository 처리 - 서버 내부에서 DB를 등록, 수정, 삭제, 조회, 저장하는 작업
* ORM 실행 → Memo 객체 → SQL 자동 생성 → SQLite 실행
* SQLite 조회 → memos 테이블 검색 → 조회 결과 반환
* 역방향 전달 SQLite -> Repository -> Service -> Router
* Template 렌더링
* HTML 응답 -> 브라우저로 전송 200 OK

---

### GET과 POST의 역할 차이와 분리하는 이유
* 만약 등록 기능 GET 만든다면 브라우저 새로고침 동일한 등록 요청 재실행 중복 저장 문제 발생 방지

| 구분       | GET          | POST         |
| -------- | ------------ | ------------ |
| 역할       |  조회       | 등록/수정/삭제       |
| 예시       | 목록 조회, 상세 조회 | 등록, 수정, 삭제   |
| DB 변경   | 없음           | 있음           |
| PRG 필요   | X           | O              |
| F5 영향 | 안전           | 중복 실행 위험     |

--- 

### HTML Form 입력값이 서버로 전달되는 과정
* 사용자 HTML Form 입력
* POST /memos 저장 버튼 클릭 - 서버 데이터 전송
* Router에서 Form 수신 - FastAPI가 자동으로 처리
* Service 전달 -> Repository 저장 -> SQLite 저장

사용자가 HTML Form에 입력한 데이터를 서버로 전송하면 FastAPI가 Form 파라미터로 값을 받아 Python 변수로 변환하고, 이후 Service와 Repository를 거쳐 데이터베이스에 저장

---

### PRG(Post-Redirect-Get) 패턴을 적용해야 하는 이유
* PRG(Post-Redirect-Get) 패턴은 사용자가 새로고침(F5)을 했을 때 등록·수정·삭제 요청이 중복 실행되는 것을 방지하기 위해 사용
* Redirect = POST 요청 처리 후 사용자를 다른 URL로 이동시켜 새로고침 시 중복 요청이 발생하지 않도록 하는 기능
```py
@router.post("/memos")
(...)
return {
        "message": "저장 완료"
    }
```

---

### SQLAlchemy
- Python에서 데이터베이스를 다루기 위한 라이브러리

### SQLAlchemy ORM
- Python 객체(Class)와 DB 테이블을 매핑하여 CRUD를 수행하는 기능

### SQLAlchemy ORM 기반 단일 모델 CRUD 동작 원리
* SQLAlchemy ORM은 Memo 클래스를 memos 테이블과 매핑하고 Repository에서 db.query() db.add() db.commit()을 사용해 SQL을 직접 작성하지 않고 CRUD를 수행

#### main.py
* FastAPI 애플리케이션 생성
* 데이터베이스 및 테이블 생성
* ORM 모델 확인 -> SQLite 테이블 생성
* database.db
* Jinja2 템플릿 설정 - templates 폴더 사용 -> HTML 렌더링 가능
* Router 등록
* 홈 화면 출력 - http://localhost:8000


#### models/memo.py
* SQLite 데이터베이스 테이블 구조 정의
* 컬럼 정의

#### database.py
* SQLite와 SQLAlchemy를 연결 관리 DB 설정 파일


#### repositories/memo_repository.py
- CRUD 수행(조회 저장 수정 삭제)


#### services/memo_service.py
- 폼 유효성 검사
- 로직 처리


#### routers/memo_router.py
- HTTP 요청/응답 처리
- GET/POST 요청 처리
- 브라우저에서 전달한 Form 데이터 수신 역할
- TemplateResponse 반환
- RedirectResponse 반환



### HTML Form()
- 사용자가 폼에 입력한 값은 HTTP 요청으로 서버에 전달되며 Jinja2 SSR 구조에서는 FastAPI의 Form() 파라미터가 이를 받아 처리

### Jinja2 SSR(Server Side Rendering)
- FastAPI 서버가 HTML을 생성해서 브라우저에 전달하는 방식

### CORS(Cross-Origin Resource Sharing)
- 다른 Origin의 서버와 통신할 수 있도록 브라우저가 허용하는 정책
- Origin 구성(프로토콜+호스트+포트)
- http://localhost:3000 <-> http://localhost:8000


