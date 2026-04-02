## docker compose
- 여러 컨테이너를 한 번에 관리하는 도구
- YAML(Yet Another Markup Language) 파일로 서비스를 정의하고 실행
- 사람이 읽기 쉽도록 설계된, 기계가 해석하기 쉬운 데이터 직렬화 언어

## 컨테이너 실행 명령이 문서화된 설정으로 바뀌는 이유

### 명령어 기반 실행 (과거)

- 명령어는 휘발성(Volatile)
    - 명령어 기록이 남지 않음
    - 팀원들이 같은 방식으로 실행하기 어려움
    - 실행 환경이 일관성 없음

- 복잡한 옵션 관리
    - 옵션이 많으면 오타 발생 확률 높음
    - 명령어를 복사-붙여넣기하기 어려움
    - 실행 순서를 관리해야 함

- 재현성(Reproducibility) 부족
    - 환경마다 다른 명령어 사용
    - 설정 차이를 추적하기 어려움
    - 버그 재현이 어려움

```bash
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  -v $(pwd):/app \
  -e FLASK_ENV=development \
  -e FLASK_APP=app.py \
  --restart unless-stopped \
  flask:latest
```

### 선언형 설정 (현재)
- 문서화 (Documentation)
    - 새로운 개발자도 파일만 읽으면 이해 가능
    - 설정 변경 이력을 Git으로 추적 가능
    - 코드 리뷰 가능

- 일관성 (Consistency)
    - 개발 환경 = 테스트 환경 = 프로덕션 환경
    - 버그 재현 가능
    - 예측 가능한 동작

- 확장성 (Scalability)
    - 서비스 추가/제거가 쉬움
    - 의존성 관리 자동화
    - 스케일링 가능

- 버전 관리 (Version Control)

    - 누가 언제 뭘 바꿨는지 추적 가능
    - 이전 버전으로 롤백 가능
    - 코드 리뷰 가능


```yaml
version: '3.8'
services:
  flask:
    image: flask:latest
    container_name: flask-app
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
      - FLASK_APP=app.py
    restart: unless-stopped
```


## docker-compose 설치
```bash
$ sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

### 실행 권한 부여
```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```

### 서비스 시작
```bash
$ docker-compose up -d
```

### 실행 상태 확인
```bash
$ docker-compose ps
```

### 로그 확인
```bash
$ docker-compose logs -f
```

### 서비스 재시작
```bash
$ docker-compose restart web
```

### 서비스 중지
```bash
$ docker-compose down
```

### 이미지 재빌드 후 시작
```bash
$ docker-compose up -d --build
```