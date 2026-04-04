## Docker Ubuntu 컨테이너
- docker attach = 메인 프로세스에 직접 연결 → 끊으면 컨테이너 종료
- 특징: 컨테이너의 메인 프로세스에만 접근 가능

- docker exec = 새 프로세스 생성 → 메인 프로세스 독립 실행
- 특징: 새로운 프로세스를 생성하므로 더 안전하고 유연함

### Ubuntu 이미지 컨테이너 생성 및 실행
```zsh
$ docker run -it --name my-ubuntu ubuntu:latest /bin/bash
```

### 현재 디렉토리의 파일/폴더 목록 표시 (숨김파일 제외)
```zsh
$ ls
```

### 현재 디렉토리의 모든 파일/폴더 상세 정보 표시 (숨김파일 포함)
```zsh
$ ls -la
```

### 텍스트 출력
```zsh
$ echo "Hello Docker!"
```

### 현재 작업 디렉토리의 절대 경로 출력
```zsh
$ pwd
```

### OS 정보 확인
```zsh
$ cat /etc/os-release
```

### 컨테이너 내 bash 셸 종료 (컨테이너도 중지됨)
```zsh
$ exit
```

### 중지된 'my-ubuntu' 컨테이너 재시작
```zsh
$ docker start my-ubuntu
```

### 실행 중인 컨테이너에 표준입력/출력 연결 (기존 프로세스에 접속)
```zsh
$ docker attach my-ubuntu
```

### 컨테이너 내 bash 셸 종료
```zsh
$ exit
```

### 중지된 컨테이너 재시작
```zsh
$ docker start my-ubuntu
```

```
attach: 메인 프로세스 제어 → exit하면 컨테이너 중지
exec: 새 프로세스 추가 → exit해도 컨테이너 유지
```

### 실행 중인 컨테이너에서 새로운 bash 프로세스 실행 (권장 방식)
```zsh
$ docker exec -it my-ubuntu /bin/bash
```

### 실행 중인 컨테이너 중지 (graceful shutdown)
```zsh
$ docker stop
```

### 컨테이너 삭제
```zsh
$ docker rm <CONTAINER ID>
```

### 컨테이너 이름으로 로그 확인
```zsh
$ docker logs my-ubuntu
```

### 컨테이너 ID로 로그 확인
```zsh
$ docker logs a1b2c3d4e5f6
```

### 실시간 로그 보기 (follow)
```zsh
$ docker logs -f my-ubuntu
```

### 마지막 10줄만 보기
```zsh
$ docker logs --tail 10 my-ubuntu
```

### 타임스탬프와 함께 보기
```zsh
$ docker logs -t my-ubuntu
```

### 마지막 10줄을 실시간으로 보기
```zsh
$ docker logs -f --tail 10 my-ubuntu
```

### 컨테이너 리소스 사용량 실시간 모니터링
```zsh
$ docker stats
```

### 특정 컨테이너 'my-ubuntu'의 리소스 사용량만 실시간 표시
```zsh
$ docker stats my-ubuntu
```

### 여러 컨테이너의 리소스 사용량을 동시에 실시간 표시
```zsh
$ docker stats my-ubuntu another-container
```