# FastAPI Memo Management Service

* FastAPI MySQL SQLAlchemy Jinja2 기반의 인증·카테고리 연관 메모 관리 웹 서비스


## 주요 기능
- 회원가입 로그인 로그아웃
- 비밀번호 bcrypt 해시 저장 및 검증
- GitHub OAuth 로그인
- Google OAuth 로그인
- 세션 기반 사용자 인증
- 사용자별 메모 CRUD
  - 목록 조회
  - 상세 조회
  - 등록
  - 수정
  - 삭제
- 메모 완료·미완료 상태 전환
- 메모 제목 검색
- 사용자별 카테고리 관리
- 메모와 카테고리 연관관계 설정
- 회원가입 시 기본 카테고리 자동 생성
  - 공부
  - 업무
  - 개인
- 존재하지 않는 메모 요청 시 404 처리
- 로그인 필요 페이지 접근 제어
- 회원가입 완료 후 성공 메시지 표시


## Deployment

* 서비스 URL: https://fastapi-memo-auth.up.railway.app/
* 회원가입: https://fastapi-memo-auth.up.railway.app/signup
* 로그인: https://fastapi-memo-auth.up.railway.app/login


## 실행

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
fastapi dev
```

개발 서버의 기본 주소는 다음과 같습니다.

```text
http://127.0.0.1:8000
```


## 테스트 계정

별도로 제공되는 고정 테스트 계정은 없습니다. `/signup`에서 직접 가입한 계정으로 다음 절차를 확인합니다.

```text
1. /signup에서 사용자 가입
2. /login에서 생성한 계정으로 로그인
3. /memos에서 메모 목록 확인
4. 메모 등록·상세 조회·수정·상태 변경·삭제 확인
5. 로그아웃 후 /memos 접근 시 /login으로 이동하는지 확인
```

회원가입이 완료되면 해당 사용자에게 `공부`, `업무`, `개인` 기본 카테고리가 생성됩니다.


## 인증·인가

### 인증(Authentication)

- 현재 요청을 보낸 사용자가 누구인지 확인
- 이 프로젝트에서는 로그인 성공 시 사용자 ID를 세션에 저장하고, 이후 요청에서 `Depends(get_current_user)`를 통해 현재 사용자를 확인합니다.

### 인가(Authorization)

- 인증된 사용자가 특정 메모에 접근하거나 수정·삭제 권한이 있는지 확인
- 메모 조회 시 `memo_id`뿐만 아니라 `current_user.id`를 함께 조건으로 사용하여 본인이 소유한 메모만 처리합니다.



## 접근 경로 정책

### 공개 경로(비로그인 사용자)

| URL                     | 방식        | 기능                  |
| ----------------------- | --------- | ------------------- |
| `/`                     | GET       | 홈 화면                |
| `/signup`               | GET POST  | 회원가입 화면 및 처리        |
| `/login`                | GET POST  | 로그인 화면 및 처리         |
| `/auth/github`          | GET       | GitHub OAuth 로그인 시작 |
| `/auth/github/callback` | GET       | GitHub OAuth 인증 콜백  |
| `/auth/google`          | GET       | Google OAuth 로그인 시작 |
| `/auth/google/callback` | GET       | Google OAuth 인증 콜백  |
| `/logo`                 | GET       | 로고 화면               |
| `/docs`                 | GET       | Swagger UI           |
| `/redoc`                | GET       | ReDoc API 문서        |
| `/openapi.json`         | GET       | OpenAPI Schema       |
| `/static/*`             | GET       | 정적 파일               |

### 보호 경로(로그인 사용자)

| URL                       | 방식        | 기능               |
| ------------------------- | --------- | ---------------- |
| `/logout`                 | POST      | 로그아웃             |
| `/memos`                  | GET       | 메모 목록 및 제목 검색    |
| `/memos`                  | POST      | 메모 등록            |
| `/memos/new`              | GET       | 메모 등록 화면         |
| `/memos/{memo_id}`        | GET       | 메모 상세 조회         |
| `/memos/{memo_id}/edit`   | GET POST  | 메모 수정 화면 및 수정 처리 |
| `/memos/{memo_id}/delete` | POST      | 메모 삭제            |
| `/memos/{memo_id}/status` | POST      | 메모 완료·미완료 상태 변경  |


보호 경로에서는 `Depends(get_current_user)`를 사용하여 현재 로그인 사용자를 확인합니다. 로그인하지 않은 사용자가 보호 경로에 접근하면 로그인 화면으로 이동합니다.

메모 상세 조회, 수정, 삭제 및 상태 변경 시에는 `memo_id`와 `current_user.id`를 함께 조회 조건으로 사용합니다. 이를 통해 현재 사용자가 소유한 메모만 처리하고, 다른 사용자의 메모에는 접근할 수 없도록 제한합니다.

`/logout`은 위 표에서 보호 경로로 분류되어 있지만, 현재 Router 함수 자체에는 로그인 의존성이 없습니다. 따라서 비로그인 상태에서도 호출할 수 있으며, 현재 세션을 비운 뒤 홈으로 이동합니다. 로그아웃을 엄격한 보호 경로로 만들려면 `require_login` 의존성과 비로그인 처리 정책을 추가해야 합니다.

FastAPI 기본 API 문서와 `/static/*` 정적 파일은 별도의 인증 검사 없이 제공됩니다. 운영 환경에서 공개하지 않아야 한다면 FastAPI 설정과 배포 계층에서 별도로 제한해야 합니다.



## 프로젝트 구조

```text
.
├── README.md                       # 프로젝트 소개, 실행 방법, 구조와 기능 설명
├── auth                            # 인증·OAuth·비밀번호 보안 처리
│   ├── auth_service.py             # 세션에서 현재 사용자 조회 및 로그인 의존성
│   ├── oauth_client.py             # GitHub·Google OAuth 클라이언트 설정
│   └── password.py                 # 비밀번호 해시 생성 및 검증
├── database.py                     # DB 엔진·세션 팩토리·get_db 의존성 정의
├── main.py                         # FastAPI 앱 미들웨어 예외처리 라우터 등록
├── models                          # SQLAlchemy ORM 모델 정의
│   ├── category.py                 # 카테고리 테이블과 연관관계 정의
│   ├── memo.py                     # 메모 테이블과 연관관계 정의
│   └── user.py                     # 사용자 테이블과 연관관계 정의
├── repositories                    # 데이터베이스 CRUD 접근 계층
│   ├── category_repository.py      # 카테고리 조회·생성 처리
│   ├── memo_repository.py          # 메모 조회·생성·수정·삭제 처리
│   └── user_repository.py          # 사용자 조회·생성 처리
├── requirements.txt                # Python 패키지 의존성 목록
├── routers                         # URL별 요청·응답 의존성 연결
│   ├── auth_router.py              # 회원가입·로그인·로그아웃·OAuth 라우팅
│   └── memo_router.py              # 메모 CRUD·검색·상태 변경 라우팅
├── services                        # 비즈니스 로직과 유효성 검사 계층
│   ├── category_service.py         # 사용자별 카테고리 비즈니스 로직
│   ├── memo_service.py             # 메모 검증·소유권 확인·상태 변경 로직
│   └── user_service.py             # 사용자 생성·인증 비즈니스 로직
├── static                          # 정적 파일
│   └── images                      
│       └── logo.png                
└── templates                       # Jinja2 서버 사이드 HTML 템플릿
    ├── 404.html                    # 리소스를 찾을 수 없을 때 표시하는 화면
    ├── home.html                   # 서비스 홈 화면
    ├── login.html                  # 로그인 화면
    ├── logo.html                   # 로고 화면
    ├── memo_detail.html            # 메모 상세 화면
    ├── memo_form.html              # 메모 등록·수정 폼
    ├── memo_list.html              # 메모 목록·검색 화면
    └── signup.html                 # 회원가입 화면
```



## 주요 의존성

| 의존성 | 활용 디렉터리·파일 | 주요 코드 및 역할 |
|---|---|---|
| `fastapi` | `main.py`, `routers/` | FastAPI 애플리케이션, 라우터, 의존성 주입, 폼 데이터 처리 |
| `uvicorn` | 애플리케이션 실행 | ASGI 기반 FastAPI 웹 서버 실행 |
| `sqlalchemy` | `database.py`, `models/`, `repositories/`, `services/`, `routers/` | MySQL 연결, ORM 모델, 세션과 트랜잭션 처리 |
| `pymysql` | `database.py` | SQLAlchemy와 MySQL 사이의 데이터베이스 드라이버 |
| `jinja2` | `main.py`, `routers/`, `templates/` | 서버 사이드 렌더링 기반 HTML 화면 출력 |
| `python-multipart` | `routers/` | `Form()`을 사용한 회원가입, 로그인, 메모 입력값 처리 |
| `starlette` | `main.py`, `routers/` | 세션 미들웨어, 요청 객체, 응답과 리다이렉트 처리 |
| `itsdangerous` | `main.py` | `SessionMiddleware`가 사용하는 세션 쿠키 서명 기능 |
| `passlib` | `auth/password.py` | 비밀번호 해시 생성과 검증 |
| `bcrypt` | `auth/password.py` | bcrypt 비밀번호 해시 알고리즘 제공 |
| `authlib` | `auth/oauth_client.py`, `routers/auth_router.py` | GitHub·Google OAuth 인증 요청과 콜백 처리 |
| `httpx` | OAuth 통신 과정 | GitHub·Google OAuth 서버와 비동기 HTTP 통신 |
| `python-dotenv` | `database.py`, `main.py`, `auth/oauth_client.py` | `.env` 파일에서 환경 변수 로드 |

