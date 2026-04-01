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

## 포트 매핑 필요한 이유
포트 매핑 = 컨테이너 서비스를 호스트를 통해 외부에서 접속 가능
포트 매핑 없으면 컨테이너 내부에서만 서비스 가능 → 외부 접근 불가능