## Dockerfile NGINX 이미지 빌드

### 빌드
```zsh
$ docker build -t my-nginx-app:1.0 .
```

### 컨테이너 실행
```zsh
$ docker run -d -p 8080:80 --name my-nginx-server my-nginx-app:1.0
```

### 포트 매핑 접속 확인
```zsh
$ docker ps
```

### 웹 브라우저 접속
```zsh
$ curl http://localhost:8080
```

### Nginx 로그 확인
```zsh
$ docker logs my-nginx-server
```

### 컨테이너 중지
```zsh
$ docker stop my-nginx-server
```

### 컨테이너 재시작
```zsh
$ docker restart my-nginx-server
```

### 컨테이너 삭제
```zsh
$ docker rm my-nginx-server
```

### 이미지 삭제
```zsh
$ docker rmi my-nginx-app:1.0
```

### 실시간 로그 확인
```zsh
$ docker logs -f my-nginx-server
```

## 컨테이너 포트 매핑 필요성
```bash
포트 매핑 전
외부 → 호스트 8080 → 컨테이너 3000 (❌)
```

```bash
포트 매핑 후
외부 → 호스트 8080 → 컨테이너 3000 (✅)
```

```bash
포트 매핑 매커니즘

외부(인터넷)
    ↓
호스트 포트 8080 ──(포트 매핑)──> 컨테이너 포트 3000
    ↑                                    ↑
  접속 가능                          앱 실행 중
```