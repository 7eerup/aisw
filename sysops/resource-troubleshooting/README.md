## 시스템 장애 분석 및 이슈 리포트

- [Issue #1 - 메모리 누수 및 제한 초과로 프로세스 강제 종료](https://github.com/7eerup/aisw/issues/1)
- [Issue #2 - CPU 과점유로 Watchdog이 동작하여 프로세스 강제 종료](https://github.com/7eerup/aisw/issues/2)
- [Issue #3 - 멀티스레드 환경에서 교착상태(Deadlock) 발생으로 프로세스 무응답](https://github.com/7eerup/aisw/issues/3)


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



## Advanced

### [Analysis] 로그 패턴 분석을 통한 스케줄링 알고리즘 추론

정상 환경에서 애플리케이션을 3회 실행하여 Thread-A, Thread-B, Thread-C의 등록 순서와 실제 실행 순서를 비교하였다.

모든 실행에서 등록 순서는 동일하게 Thread-A → Thread-B → Thread-C였지만, 실제 실행 순서는 Thread-B → Thread-C → Thread-A로 나타났다.

### 로그 관찰 개요

```text
MEMORY_LIMIT=512MB
CPU_MAX_OCCUPY=50%
MULTI_THREAD_ENABLE=False
```
### 실행 순서 및 타임스탬프 분석

| 실행  | 등록 순서     | 실제 실행 순서  |
| --- | --------- | --------- |
| 1회차 | A → B → C | B → C → A |
| 2회차 | A → B → C | B → C → A |
| 3회차 | A → B → C | B → C → A |


### Round-Robin / FCFS / Priority 비교
| 알고리즘        | 특징                          | 실제 로그와 비교                                 |
| ----------- | --------------------------- | ----------------------------------------- |
| Round-Robin | 일정 Time Quantum마다 작업을 순환 실행 | 작업 간 교대가 없어 일치하지 않음                       |
| FCFS        | 먼저 도착한 작업부터 순서대로 실행         | 등록 순서 `A → B → C`와 실행 순서가 달라 단순 FCFS와 불일치 |
| Priority    | 우선순위가 높은 작업부터 실행            | 3회 모두 `B → C → A`로 실행되어 가장 유사             |



### 스케줄링 알고리즘 추론
Thread-B → Thread-C → Thread-A
현재 로그 패턴은 세 방식 중 Priority Scheduling에 가장 가까운 것으로 추론된다.

### 장단점 분석
Priority Scheduling의 장점은 중요도가 높은 작업을 먼저 처리할 수 있다는 점이다. 긴급 작업이나 핵심 서비스 요청을 우선 처리해야 하는 환경에서 효과적이며, 작업의 중요도에 따라 실행 순서를 제어할 수 있다.
반면 낮은 우선순위의 작업이 계속 뒤로 밀리는 Starvation 문제가 발생할 수 있다. 또한 우선순위 설정이 적절하지 않으면 특정 작업에 실행 기회가 집중될 수 있으므로 Aging과 같은 보완 정책이 필요할 수 있다.

### 적합한 서비스 아키텍처
Priority Scheduling은 모든 작업을 동일하게 처리하기보다 중요도에 따라 처리 순서를 결정해야 하는 서비스에 적합하다.

- 장애 복구나 긴급 작업을 우선 처리하는 시스템
- 중요도에 따라 메시지를 처리하는 Queue Worker
- 실시간 요청과 일반 Batch 작업이 함께 존재하는 서비스
- 작업 등급에 따라 처리 순서를 결정하는 Backend Worker
- 운영·모니터링 이벤트 중 Critical 이벤트를 먼저 처리하는 시스템

### 결론

상 환경에서 애플리케이션을 3회 실행한 결과, 등록 순서는 Thread-A → Thread-B → Thread-C였지만 실제 실행 순서는 모두 Thread-B → Thread-C → Thread-A로 동일하였다.
각 Thread가 작업을 끝까지 완료한 후 다음 Thread가 실행되므로 Round-Robin 방식과는 차이가 있었고, 등록 순서와 실제 실행 순서가 다르므로 단순 FCFS 방식과도 일치하지 않았다.
따라서 반복적으로 동일한 B → C → A 실행 순서가 나타난 점을 근거로, 현재 프로그램은 Priority Scheduling 방식에 가장 가까운 것으로 추론된다.



### 결과
```
2026-08-30 17:24:12,430 [INFO] [Scheduler] Registered Tasks: ['Thread-A', 'Thread-B', 'Thread-C']
2026-08-30 17:24:12,430 [INFO] [Scheduler] Starting task execution...
2026-08-30 17:24:12,430 [INFO] [Thread-B] Task Started. Calculating... (20%)
2026-08-30 17:24:12,482 [INFO] [Thread-B] Calculating... (40%)
2026-08-30 17:24:12,534 [INFO] [Thread-B] Calculating... (60%)
2026-08-30 17:24:12,586 [INFO] [Thread-B] Calculating... (80%)
2026-08-30 17:24:12,638 [INFO] [Thread-B] Task Completed. (100%)
2026-08-30 17:24:12,689 [INFO] [Thread-C] Task Started. Calculating... (20%)
2026-08-30 17:24:12,741 [INFO] [Thread-C] Calculating... (40%)
2026-08-30 17:24:12,793 [INFO] [Thread-C] Calculating... (60%)
2026-08-30 17:24:12,845 [INFO] [Thread-C] Calculating... (80%)
2026-08-30 17:24:12,896 [INFO] [Thread-C] Task Completed. (100%)
2026-08-30 17:24:12,948 [INFO] [Thread-A] Task Started. Calculating... (20%)
2026-08-30 17:24:13,000 [INFO] [Thread-A] Calculating... (40%)
2026-08-30 17:24:13,052 [INFO] [Thread-A] Calculating... (60%)
2026-08-30 17:24:13,103 [INFO] [Thread-A] Calculating... (80%)
2026-08-30 17:24:13,154 [INFO] [Thread-A] Task Completed. (100%)
2026-08-30 17:24:13,205 [INFO] [Scheduler] All tasks completed.









2026-08-30 17:28:13,265 [INFO] [Scheduler] Registered Tasks: ['Thread-A', 'Thread-B', 'Thread-C']
2026-08-30 17:28:13,265 [INFO] [Scheduler] Starting task execution...
2026-08-30 17:28:13,265 [INFO] [Thread-B] Task Started. Calculating... (20%)
2026-08-30 17:28:13,317 [INFO] [Thread-B] Calculating... (40%)
2026-08-30 17:28:13,368 [INFO] [Thread-B] Calculating... (60%)
2026-08-30 17:28:13,420 [INFO] [Thread-B] Calculating... (80%)
2026-08-30 17:28:13,472 [INFO] [Thread-B] Task Completed. (100%)
2026-08-30 17:28:13,524 [INFO] [Thread-C] Task Started. Calculating... (20%)
2026-08-30 17:28:13,575 [INFO] [Thread-C] Calculating... (40%)
2026-08-30 17:28:13,627 [INFO] [Thread-C] Calculating... (60%)
2026-08-30 17:28:13,678 [INFO] [Thread-C] Calculating... (80%)
2026-08-30 17:28:13,729 [INFO] [Thread-C] Task Completed. (100%)
2026-08-30 17:28:13,781 [INFO] [Thread-A] Task Started. Calculating... (20%)
2026-08-30 17:28:13,833 [INFO] [Thread-A] Calculating... (40%)
2026-08-30 17:28:13,885 [INFO] [Thread-A] Calculating... (60%)
2026-08-30 17:28:13,937 [INFO] [Thread-A] Calculating... (80%)
2026-08-30 17:28:13,988 [INFO] [Thread-A] Task Completed. (100%)
2026-08-30 17:28:14,040 [INFO] [Scheduler] All tasks completed.











2026-08-30 17:30:39,532 [INFO] [Scheduler] Registered Tasks: ['Thread-A', 'Thread-B', 'Thread-C']
2026-08-30 17:30:39,532 [INFO] [Scheduler] Starting task execution...
2026-08-30 17:30:39,533 [INFO] [Thread-B] Task Started. Calculating... (20%)
2026-08-30 17:30:39,584 [INFO] [Thread-B] Calculating... (40%)
2026-08-30 17:30:39,635 [INFO] [Thread-B] Calculating... (60%)
2026-08-30 17:30:39,687 [INFO] [Thread-B] Calculating... (80%)
2026-08-30 17:30:39,738 [INFO] [Thread-B] Task Completed. (100%)
2026-08-30 17:30:39,790 [INFO] [Thread-C] Task Started. Calculating... (20%)
2026-08-30 17:30:39,842 [INFO] [Thread-C] Calculating... (40%)
2026-08-30 17:30:39,893 [INFO] [Thread-C] Calculating... (60%)
2026-08-30 17:30:39,945 [INFO] [Thread-C] Calculating... (80%)
2026-08-30 17:30:39,997 [INFO] [Thread-C] Task Completed. (100%)
2026-08-30 17:30:40,049 [INFO] [Thread-A] Task Started. Calculating... (20%)
2026-08-30 17:30:40,100 [INFO] [Thread-A] Calculating... (40%)
2026-08-30 17:30:40,152 [INFO] [Thread-A] Calculating... (60%)
2026-08-30 17:30:40,203 [INFO] [Thread-A] Calculating... (80%)
2026-08-30 17:30:40,254 [INFO] [Thread-A] Task Completed. (100%)
2026-08-30 17:30:40,305 [INFO] [Scheduler] All tasks completed.
```