# FastAPI CRUD Memo Service

* FastAPI와 SQLAlchemy를 활용하여 구현한 메모 관리 웹 서비스
* CRUD = 소프트웨어와 데이터베이스에서 데이터를 처리하는 4가지 기본 기능인 생성(Create), 읽기(Read), 수정(Update), 삭제(Delete)

---

##
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "fastapi[standard]" sqlalchemy
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
    └── 404.html
```

---


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

## 브라우저 요청 FastAPI 서버에서 "라우터 → 서비스 → 저장소 → 템플릿" 흐름
- 사용자가 저장 버튼을 클릭하면 POST /memos 요청이 발생한다. FastAPI는 Form 데이터를 읽고 타입 검증을 수행한 뒤 Router의 memo_create()를 실행한다. Router는 Service의 create_memo()를 호출하고, Service에서는 제목과 내용이 비어 있는지 검증한다. 검증에 실패하면 ValueError를 발생시키고, 성공하면 Repository의 save()를 호출한다. Repository에서는 Memo 객체를 생성하고 add(), commit(), refresh()를 통해 DB에 저장한다. 저장이 완료되면 RedirectResponse(303)를 반환하고 브라우저는 GET /memos를 다시 요청하여 목록 화면을 렌더링한다.

```python
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
```

---

### GET과 POST의 역할 차이와 분리하는 이유
- GET - 서버에서 데이터를 조회(Read)하기 위한 요청 방식
- @router.get("/memos") 목록 조회
- @router.get("/memos/new") 등록 화면
- @router.get("/memos/{memo_id}") 상세 조회

- POST - 서버에 새로운 데이터를 Create Update Delete 처리하기 위한 요청 방식
- @router.post("/memos") 생성
- @router.post("/memos/{memo_id}/edit") 수정
- @router.post("/memos/{memo_id}/delete") 삭제
- 만약 등록 기능 GET 만든다면 브라우저 새로고침 동일한 등록 요청 재실행 중복 저장 문제 발생 방지


메모 생성(Create)
사용자 입력 → 저장 버튼 클릭 → POST /memos → Router → Service → Repository → SQLAlchemy ORM → DB INSERT → RedirectResponse(303) → GET /memos → 목록 화면 출력


메모 목록 조회(Read)
브라우저 접속 → GET /memos → Router → Service → Repository → SQLAlchemy ORM → SELECT * FROM memos → Jinja2 TemplateResponse → HTML 렌더링 → 브라우저 출력


메모 수정(Update)
수정 버튼 클릭 → GET /memos/{id}/edit → 수정 화면 출력 → 저장 버튼 클릭 → POST /memos/{id}/edit → Router → Service → Repository → UPDATE memos → RedirectResponse(303) → GET /memos → 목록 출력


메모 삭제(Delete)
삭제 버튼 클릭 → POST /memos/{id}/delete → Router → Service → Repository → DELETE FROM memos → RedirectResponse(303) → GET /memos → 목록 출력


--- 

### HTML Form 입력값이 서버로 전달되는 과정
* 사용자 HTML Form 입력 -> POST /memos 저장 버튼 클릭 - 서버 데이터 전송 -> Router에서 Form 수신 FastAPI가 자동으로 처리 -> Service 전달 -> Repository 저장 -> SQLite 저장

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
- SQLAlchemy Session의 query()는 SELECT 조회, add()는 INSERT 대상 등록, commit()은 실제 INSERT·UPDATE·DELETE를 데이터베이스에 반영하는 역할을 한다. 또한 delete()는 삭제 대상을 등록하고, refresh()는 저장 후 데이터베이스의 최신 상태를 다시 조회하여 객체에 반영한다.

### SQLAlchemy ORM 기반 단일 모델 CRUD 동작 원리
* SQLAlchemy ORM은 Memo 클래스를 memos 테이블과 매핑하고 Repository에서 db.query() db.add() db.commit()을 사용해 SQL을 직접 작성하지 않고 CRUD를 수행

---

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

---

### Jinja2 SSR(Server Side Rendering)
- FastAPI 서버가 HTML을 생성해서 브라우저에 전달하는 방식

### CORS(Cross-Origin Resource Sharing)
- 다른 Origin의 서버와 통신할 수 있도록 브라우저가 허용하는 정책
- Origin 구성(프로토콜+호스트+포트)
- http://localhost:3000 <-> http://localhost:8000


---

### Advanced Functions
- Router - keyword 쿼리 파라미터 받기
- Service - 검색어를 Repository로 전달
- Repository - SQLAlchemy filter()와 like()로 제목 포함 검색 수행
- Template - 검색 입력창과 결과 목록 출력

- 목록 화면에서 검색어를 입력하면 GET /memos?keyword=검색어 요청이 발생하고, Router가 keyword를 받아 Service를 거쳐 Repository에서 Memo.title.like("%검색어%") 조건으로 DB를 조회한 뒤 결과를 다시 memo_list.html에 렌더링한다.


- 간단한 검증 기능은 Service 계층에서 수동 검증 방식으로 구현하였다. 사용자가 저장 버튼을 클릭하면 Router가 Form 데이터를 받아 Service의 create_memo()를 호출한다. Service에서는 title.strip()과 content.strip()을 사용하여 필수값 입력 여부를 확인하고, 값이 비어 있으면 ValueError를 발생시킨다. Router는 해당 예외를 처리하여 TemplateResponse로 다시 입력 화면을 반환하고, error 메시지를 화면에 출력한다. 검증을 통과한 경우에만 Repository의 save()가 호출되어 DB에 저장된다.

- onsubmit = 폼 제출 이벤트