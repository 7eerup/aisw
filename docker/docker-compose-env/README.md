## Docker Compose ENV
- docker compose CMD 실행
- --env-file: 어떤 환경변수를 쓸지 결정
- --profile: 어떤 서비스를 실행할지 결정
- up --build: 빌드 + 실행 동시 처리
- docker compose up -d --build (X)
- docker compose --env-file .env.dev up -d --build (O)
- 환경 변수 활용 경우 --env-file 플래그는 필수

### 이미지 빌드 업
```bash
$ docker compose --env-file .env.dev --profile dev up --build
```

### 로그
```bash
$ docker compose --env-file .env.dev --profile dev logs -f
```

### 재시작
```bash
$ docker compose --env-file .env.dev --profile dev restart
```

### 종료
```bash
$ docker compose --env-file .env.dev --profile dev down
```

### 테스트
```bash
$ curl http://localhost:8000/
{"message":"Hello","mode":"development","port":8000}
```

http://localhost:8000/docs
http://localhost:8000/redoc


### 빌드
```bash
$ docker compose --env-file .env.prod --profile prod up --build
```

### 로그
```bash
$ docker compose --env-file .env.prod --profile prod logs -f
```

### 재시작
```bash
$ docker compose --env-file .env.prod --profile prod restart
```

### 종료
```bash
$ docker compose --env-file .env.prod --profile prod down
```

### 테스트
```bash
$ curl http://localhost:3000/
{"message":"Hello","mode":"production","port":3000}
```

http://localhost:3000/docs
http://localhost:3000/redoc