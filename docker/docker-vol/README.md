## Docker Volume 영속성 검증
- Docker 볼륨 컨테이너 외부에 데이터를 저장하는 메커니즘
- 영속성 컨테이너가 삭제되어도 데이터가 유지됨
- Mountpoint 호스트 시스템에서 실제 데이터가 저장되는 경로
- -v 옵션 볼륨을 컨테이너에 연결하는 명령어
- Mountpoint 경로가 실제 데이터가 저장되는 위치

### 생성
```zsh
$ docker volume create my-data
```

### 볼륨 목록 확인
```zsh
$ docker volume inspect my-data
```

### 컨테이너 생성 및 볼륨 연결
```zsh
$ docker run -d --name test-container \
  -v my-data:/app/data \
  ubuntu:22.04 \
  sleep 3600
```

### 컨테이너 내부에서 데이터 생성
```zsh
$ docker exec test-container bash -c \
  'echo "Hello Docker!" > /app/data/test.txt'
```

### 컨테이너 내부 추가 데이터 생성
```zsh
$ docker exec test-container bash -c \
  'echo "파일 1" > /app/data/file1.txt && \
   echo "파일 2" > /app/data/file2.txt && \
   echo "파일 3" > /app/data/file3.txt'
```

### 컨테이너 내부 추가 데이터 생성
```zsh
$ docker exec test-container ls -la /app/data/
```

### 컨테이너 삭제
```zsh
$ docker stop test-container
$ docker rm test-container
```

### 볼륨 데이터 확인
```zsh
$ docker volume inspect my-data
```

### 새로운 컨테이너로 기존 데이터 확인
```zsh
$ docker run -it --name verify-container \
  -v my-data:/app/data \
  ubuntu:22.04 \
  bash
  ```

### 컨테이너 삭제
```zsh
$ docker stop verify-container
$ docker rm verify-container
```

### 목록 확인
```zsh
$ docker volume ls
```