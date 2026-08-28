## OOM/Memory Leak, CPU 과점유, Deadlock 3가지 장애 재현·관측·분석 환경 변수 변경 전후 비교


### 트러블슈팅용 애플리케이션 배치

```bash
sudo cp agent-app-leak-x86 /home/agent-admin/agent-app/
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/agent-app-leak-x86
sudo chmod 750 /home/agent-admin/agent-app/agent-app-leak-x86
sudo ls -l /home/agent-admin/agent-app/agent-app-leak-x86
```


### 트러블슈팅용 환경 변수 등록

```bash
sudo -u agent-admin sh -c 'echo "export MEMORY_LIMIT=256" >> /home/agent-admin/.bashrc'
sudo -u agent-admin sh -c 'echo "export CPU_MAX_OCCUPY=50" >> /home/agent-admin/.bashrc'
sudo -u agent-admin sh -c 'echo "export MULTI_THREAD_ENABLE=true" >> /home/agent-admin/.bashrc'

sudo tail -n 8 /home/agent-admin/.bashrc
```


### 환경 변수 적용 확인
```bash
sudo -iu agent-admin
whoami
env | grep -E '^AGENT_|^MEMORY_LIMIT|^CPU_MAX_OCCUPY|^MULTI_THREAD_ENABLE'
```


### 필수 경로·키 파일·로그 권한 확인
```bash
ls -ld $AGENT_HOME
ls -ld $AGENT_UPLOAD_DIR
ls -ld $AGENT_KEY_PATH
ls -ld $AGENT_LOG_DIR
ls -l $AGENT_KEY_PATH/secret.key
cat $AGENT_KEY_PATH/secret.key
test -w $AGENT_LOG_DIR && echo "LOG DIR writable: OK"
```

