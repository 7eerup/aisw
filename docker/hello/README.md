## Docker 컨테이너 실습 명령어 가이드
- Docker version 28.5.2, build ecc6942

### 이미지 실행
```bash
$ docker run hello-world
```

### 이미지 확인
```bash
$ docker images
```

### 컨테이너 실행 목록 확인
```bash
$ docker ps
```

### 특정 이미지 정보 확인
```bash
$ docker inspect hello-world
```

### 이미지 상세 정보 확인
```bash
$ docker image inspect hello-world
```

### 컨테이너 삭제
```bash
$ docker rm <CONTAINER ID>
```

### 이미지 삭제
```bash
$ docker rmi <IMAGE ID>
```