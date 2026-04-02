## 바인드 마운트(Bind Mount)
- 바인드 마운트는 호스트의 파일이나 디렉토리를 컨테이너 내부에 연결하는 방식
- 호스트의 /home/user/data  ──→  컨테이너의 /app/data
- 양방향 공유	호스트와 컨테이너가 같은 파일을 공유
- 경로 지정	호스트의 절대 경로를 명시해야 함
- 실시간 동기화	한쪽에서 파일 수정 → 다른 쪽에서 즉시 반영


### 바인드 마운트로 컨테이너 실행
```zsh
$ docker run -it -v $(pwd):/data ubuntu bash
```

### 컨테이너 내부에서 확인
```zsh
$ ls -al /
```

### 양방향 동기화 테스트
```zsh
$ echo "Hello from Container!" > /data/container.txt
```

### 호스트에서 확인
```zsh
$ cat ~/bind-mount-test/container.txt
```

# 다시 컨테이너 실행
```zsh
$ docker run -it -v $(pwd):/data ubuntu bash
```