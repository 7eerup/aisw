## Advanced Functions

- Router - keyword 쿼리 파라미터 받기
- Service - 검색어를 Repository로 전달
- Repository - SQLAlchemy filter()와 like()로 제목 포함 검색 수행
- Template - 검색 입력창과 결과 목록 출력

- 목록 화면에서 검색어를 입력하면 GET /memos?keyword=검색어 요청이 발생하고, Router가 keyword를 받아 Service를 거쳐 Repository에서 Memo.title.like("%검색어%") 조건으로 DB를 조회한 뒤 결과를 다시 memo_list.html에 렌더링한다.


- 간단한 검증 기능은 Service 계층에서 수동 검증 방식으로 구현하였다. 사용자가 저장 버튼을 클릭하면 Router가 Form 데이터를 받아 Service의 create_memo()를 호출한다. Service에서는 title.strip()과 content.strip()을 사용하여 필수값 입력 여부를 확인하고, 값이 비어 있으면 ValueError를 발생시킨다. Router는 해당 예외를 처리하여 TemplateResponse로 다시 입력 화면을 반환하고, error 메시지를 화면에 출력한다. 검증을 통과한 경우에만 Repository의 save()가 호출되어 DB에 저장된다.

- onsubmit = 폼 제출 이벤트

### 전역 예외 처리

- memo_service.py
- raise ResourceNotFoundError("해당 메모를 찾을 수 없습니다.")
- FastAPI가 예외 감지
- main.py의 @app.exception_handler(ResourceNotFoundError) 선택
- resource_not_found_handler() 실행
- 404.html 반환


### 일반 HTTP 404 처리
- 존재하지 않는 URL을 입력 http://127.0.0.1:8000/abcdef
- FastAPI 내부에서 StarletteHTTPException 404 Not Found 발생



### 검색 / 필터 기능
- 브라우저 /memos?keyword=FastAPI
- memo_router.py → keyword 쿼리 파라미터 수신
- memo_service.py → 사용자 ID와 검색 조건 전달
- memo_repository.py → keyword 유무에 따라 SQLAlchemy where 조건 추가
- MySQL 조회



### 비밀번호 해싱 및 회원가입
- passlib = 비밀번호 해싱·검증을 편리하게 관리하는 라이브러리
- bcrypt = 실제 비밀번호를 해시하는 bcrypt 알고리즘 구현체

- POST /signup → routers/auth_router.py 입력값 검증 및 중복 사용자 확인

- services/user_service.py → 사용자 생성 흐름 및 비밀번호 해시 처리

- auth/password.py → bcrypt 해시 생성

- repositories/user_repository.py → 사용자 DB 저장

- MySQL 해시된 비밀번호 저장

- routers/auth_router.py → /login?signup=success 로 303 Redirect

- templates/login.html → 회원가입 완료 메시지 출력


### Railway Deployment

- railway login
- railway status
- railway connect