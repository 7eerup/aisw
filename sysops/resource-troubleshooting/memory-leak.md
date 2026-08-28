## Memory Leak / OOM Case - Before

- PID	Process ID=현재 프로세스의 고유 번호
- PPID	Parent Process ID=이 프로세스를 만든 부모 프로세스의 PID
- %CPU	CPU 사용률=해당 프로세스가 CPU를 얼마나 사용 중인지
- %MEM	메모리 사용률=전체 물리 메모리 중 해당 프로세스가 차지하는 비율
- RSS	Resident Set Size=실제 RAM에 올라가 있는 메모리 사용량, 보통 KB
- VSZ	Virtual Memory Size=프로세스가 사용하는 전체 가상 메모리 공간, 보통 KB
- ELAPSED	실행 경과 시간=프로세스가 시작된 뒤 얼마나 지났는지


| 항목                  | Before       | After              |
| ------------------- | ------------ | ------------------ |
| MEMORY_LIMIT        | 256MB        | 512MB              |
| CPU_MAX_OCCUPY      | 50%          | 50%                |
| MULTI_THREAD_ENABLE | False        | False              |
| Heap 증가             | 25MB → 275MB | 25MB → 525MB       |
| 제한 도달 시 처리          | MemoryGuard  | Cleanup            |
| Self-Terminated     | 발생           | 발생하지 않음            |
| 최종 상태               | Killed       | Process Stabilized |


### 실험 조건

- 실행 계정: `agent-admin`
- 실행 파일: `agent-app-leak-x86`
- `MEMORY_LIMIT=256MB`
- `CPU_MAX_OCCUPY=50%`
- `MULTI_THREAD_ENABLE=False`


### Boot Sequence 확인

```text
>>> Starting Agent Boot Sequence...
[1/6] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/6] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/6] Checking Required Files             [OK]
   ... Verified 'secret.key' with correct key string.
[4/6] Checking Port Availability          [OK]
   ... Port 15034 is available.
[5/6] Verifying Log Permission            [OK]
   ... Log directory is writable: /var/log/agent-app
[6/6] Verifying Mission Environment       [OK]
   ... MEMORY_LIMIT=256MB, CPU_MAX_OCCUPY=50%, MULTI_THREAD_ENABLE=False
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
2026-08-28 15:00:28,813 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-08-28 15:00:28,813 [INFO] Agent listening at port 15034

==================================================
 [ Agent Initiate ] Resource Check 
==================================================
 [ MEMORY ] Limit: 256MB 		[ WARNING: Recommend Over 256MB ]
 [ CPU    ] Limit: 50%  		[ OK ]
 [ THREAD ] Concurrency: False 		[ OK ]
--------------------------------------------------
 >>> SYSTEM STATUS: STABLE. STARTING WORKLOAD MONITORING...
==================================================

2026-08-28 15:00:30,862 [INFO] [MemoryWorker] Current Heap: 25MB
2026-08-28 15:00:33,916 [INFO] [MemoryWorker] Current Heap: 50MB
2026-08-28 15:00:36,970 [INFO] [MemoryWorker] Current Heap: 75MB
2026-08-28 15:00:40,027 [INFO] [MemoryWorker] Current Heap: 100MB
2026-08-28 15:00:43,080 [INFO] [MemoryWorker] Current Heap: 125MB
2026-08-28 15:00:46,121 [INFO] [MemoryWorker] Current Heap: 150MB
2026-08-28 15:00:49,174 [INFO] [MemoryWorker] Current Heap: 175MB
2026-08-28 15:00:52,228 [INFO] [MemoryWorker] Current Heap: 200MB
2026-08-28 15:00:55,267 [INFO] [MemoryWorker] Current Heap: 225MB
2026-08-28 15:00:58,322 [INFO] [MemoryWorker] Current Heap: 250MB
2026-08-28 15:01:01,376 [INFO] [MemoryWorker] Current Heap: 275MB
2026-08-28 15:01:01,376 [CRITICAL] [MemoryGuard] Memory limit exceeded (275MB >= 256MB) / (Recommend Over 256MB)
2026-08-28 15:01:01,376 [CRITICAL] [MemoryGuard] Self-terminating process 3225 to prevent system instability.


>>> [SYSTEM] SELF-TERMINATED (Memory Limit Exceeded) <<<

Killed
```


### 프로세스 확인
```bash
pgrep -af agent-app-leak-x86
```

```text
3224 ./agent-app-leak-x86
3225 ./agent-app-leak-x86
```

### 초기 프로세스 메모리 사용량 확인
```bash
ps -C agent-app-leak-x86 -o pid,ppid,%cpu,%mem,rss,vsz,etime,cmd
```


```text
PID   PPID  %CPU  %MEM    RSS     VSZ     ELAPSED
3224  3168   0.2   0.0    2184    2904    00:21
3225  3224   1.3   1.2  197836  207536    00:21
```

### 이후 프로세스 메모리 사용량 확인
```bash
watch -n 3 "ps -C agent-app-leak-x86 -o pid,ppid,%cpu,%mem,rss,vsz,etime"
```

```text
PID   PPID  %CPU  %MEM    RSS     VSZ     ELAPSED
3224  3168   0.1   0.0    2184    2904    00:30
3225  3224   1.3   1.6  274648  284348    00:30
```


### Memory Leak 증거

```text
자식 프로세스 PID: 3225

RSS 초기값 : 197836 KB
RSS 이후값 : 274648 KB
증가량     : 76812 KB
```




### Before 핵심 결론

MEMORY_LIMIT=256MB, CPU_MAX_OCCUPY=50%, MULTI_THREAD_ENABLE=False
환경에서 애플리케이션 실행 후 Heap 사용량이 25MB → 275MB까지 지속적으로 증가하였다.

운영체제 수준에서도 자식 프로세스 3225의 RSS가
197836KB → 274648KB로 증가하였다.

Heap 사용량이 설정된 MEMORY_LIMIT=256MB를 초과하자
MemoryGuard가 이를 감지하고 자식 프로세스 3225를 강제 종료하였다.

따라서 Before 환경에서는 Memory Leak으로 인해 메모리 제한값을 초과하고
프로세스가 Self-Terminate 되는 OOM 장애가 재현되었다.












## Memory Leak / OOM Case - After

### 실험 조건

- 실행 계정: `agent-admin`
- 실행 파일: `agent-app-leak-x86`
- `MEMORY_LIMIT=512MB`
- `CPU_MAX_OCCUPY=50%`
- `MULTI_THREAD_ENABLE=False`

### Boot Sequence 확인


```text
>>> Starting Agent Boot Sequence...
[1/6] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/6] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/6] Checking Required Files             [OK]
   ... Verified 'secret.key' with correct key string.
[4/6] Checking Port Availability          [OK]
   ... Port 15034 is available.
[5/6] Verifying Log Permission            [OK]
   ... Log directory is writable: /var/log/agent-app
[6/6] Verifying Mission Environment       [OK]
   ... MEMORY_LIMIT=512MB, CPU_MAX_OCCUPY=50%, MULTI_THREAD_ENABLE=False
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
2026-08-28 15:05:27,771 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-08-28 15:05:27,771 [INFO] Agent listening at port 15034

==================================================
 [ Agent Initiate ] Resource Check 
==================================================
 [ MEMORY ] Limit: 512MB 		[ OK ]
 [ CPU    ] Limit: 50%  		[ OK ]
 [ THREAD ] Concurrency: False 		[ OK ]
--------------------------------------------------
 >>> SYSTEM STATUS: STABLE. STARTING WORKLOAD MONITORING...
==================================================

2026-08-28 15:05:29,781 [INFO] >>> Scenario Selected: [Healthy System Monitoring]

>>> [SYSTEM] ALL CONFIGURATIONS OPTIMAL. RUNNING STABILITY TEST... <<<

2026-08-28 15:05:29,782 [INFO] [Scheduler] Task Scheduler Initialized.
2026-08-28 15:05:29,782 [INFO] [Scheduler] Registered Tasks: ['Thread-A', 'Thread-B', 'Thread-C']
2026-08-28 15:05:29,782 [INFO] [Scheduler] Starting task execution...
2026-08-28 15:05:29,783 [INFO] [Thread-B] Task Started. Calculating... (20%)
2026-08-28 15:05:29,834 [INFO] [Thread-B] Calculating... (40%)
2026-08-28 15:05:29,886 [INFO] [Thread-B] Calculating... (60%)
2026-08-28 15:05:29,937 [INFO] [Thread-B] Calculating... (80%)
2026-08-28 15:05:29,989 [INFO] [Thread-B] Task Completed. (100%)
2026-08-28 15:05:30,040 [INFO] [Thread-C] Task Started. Calculating... (20%)
2026-08-28 15:05:30,092 [INFO] [Thread-C] Calculating... (40%)
2026-08-28 15:05:30,144 [INFO] [Thread-C] Calculating... (60%)
2026-08-28 15:05:30,195 [INFO] [Thread-C] Calculating... (80%)
2026-08-28 15:05:30,246 [INFO] [Thread-C] Task Completed. (100%)
2026-08-28 15:05:30,298 [INFO] [Thread-A] Task Started. Calculating... (20%)
2026-08-28 15:05:30,349 [INFO] [Thread-A] Calculating... (40%)
2026-08-28 15:05:30,400 [INFO] [Thread-A] Calculating... (60%)
2026-08-28 15:05:30,451 [INFO] [Thread-A] Calculating... (80%)
2026-08-28 15:05:30,503 [INFO] [Thread-A] Task Completed. (100%)
2026-08-28 15:05:30,554 [INFO] [Scheduler] All tasks completed.
2026-08-28 15:05:30,572 [INFO] [MemoryWorker] Current Heap: 25MB
2026-08-28 15:05:30,572 [INFO] [CpuWorker] Started. Maximum CPU Limit: 50%
2026-08-28 15:05:30,572 [INFO] [CpuWorker] Current Load: 5.00%
2026-08-28 15:05:33,627 [INFO] [MemoryWorker] Current Heap: 50MB
2026-08-28 15:05:33,692 [INFO] [CpuWorker] Current Load: 11.21%
2026-08-28 15:05:36,666 [INFO] [MemoryWorker] Current Heap: 75MB
2026-08-28 15:05:36,811 [INFO] [CpuWorker] Current Load: 19.29%
2026-08-28 15:05:39,713 [INFO] [MemoryWorker] Current Heap: 100MB
2026-08-28 15:05:39,930 [INFO] [CpuWorker] Current Load: 23.47%
2026-08-28 15:05:42,765 [INFO] [MemoryWorker] Current Heap: 125MB
2026-08-28 15:05:43,046 [INFO] [CpuWorker] Current Load: 25.01%
2026-08-28 15:05:45,819 [INFO] [MemoryWorker] Current Heap: 150MB
2026-08-28 15:05:46,163 [INFO] [CpuWorker] Current Load: 30.52%
2026-08-28 15:05:48,873 [INFO] [MemoryWorker] Current Heap: 175MB
2026-08-28 15:05:49,281 [INFO] [CpuWorker] Current Load: 35.87%
2026-08-28 15:05:51,929 [INFO] [MemoryWorker] Current Heap: 200MB
2026-08-28 15:05:52,398 [INFO] [CpuWorker] Current Load: 40.51%
2026-08-28 15:05:54,982 [INFO] [MemoryWorker] Current Heap: 225MB
2026-08-28 15:05:55,518 [INFO] [CpuWorker] Current Load: 43.30%
2026-08-28 15:05:58,040 [INFO] [MemoryWorker] Current Heap: 250MB
2026-08-28 15:05:58,634 [INFO] [CpuWorker] Current Load: 48.06%
2026-08-28 15:06:00,747 [INFO] [CpuWorker] Peak reached (50.00%). Starting cooldown...
2026-08-28 15:06:01,090 [INFO] [MemoryWorker] Current Heap: 275MB
2026-08-28 15:06:01,754 [INFO] [CpuWorker] Current Load: 50.00%
2026-08-28 15:06:04,137 [INFO] [MemoryWorker] Current Heap: 300MB
2026-08-28 15:06:04,872 [INFO] [CpuWorker] Current Load: 40.62%
2026-08-28 15:06:07,191 [INFO] [MemoryWorker] Current Heap: 325MB
2026-08-28 15:06:07,986 [INFO] [CpuWorker] Current Load: 32.42%
2026-08-28 15:06:10,244 [INFO] [MemoryWorker] Current Heap: 350MB
2026-08-28 15:06:11,105 [INFO] [CpuWorker] Current Load: 29.80%
2026-08-28 15:06:13,298 [INFO] [MemoryWorker] Current Heap: 375MB
2026-08-28 15:06:14,225 [INFO] [CpuWorker] Current Load: 24.15%
2026-08-28 15:06:16,354 [INFO] [MemoryWorker] Current Heap: 400MB
2026-08-28 15:06:17,360 [INFO] [CpuWorker] Current Load: 18.15%
2026-08-28 15:06:19,407 [INFO] [MemoryWorker] Current Heap: 425MB
2026-08-28 15:06:20,482 [INFO] [CpuWorker] Current Load: 8.62%
2026-08-28 15:06:22,455 [INFO] [MemoryWorker] Current Heap: 450MB
2026-08-28 15:06:22,595 [INFO] [CpuWorker] Cooldown complete (5.00%). Resuming load increase...
2026-08-28 15:06:23,601 [INFO] [CpuWorker] Current Load: 5.00%
2026-08-28 15:06:25,505 [INFO] [MemoryWorker] Current Heap: 475MB
2026-08-28 15:06:26,720 [INFO] [CpuWorker] Current Load: 10.15%
2026-08-28 15:06:28,560 [INFO] [MemoryWorker] Current Heap: 500MB
2026-08-28 15:06:29,841 [INFO] [CpuWorker] Current Load: 17.23%
2026-08-28 15:06:31,616 [INFO] [MemoryWorker] Current Heap: 525MB
2026-08-28 15:06:31,617 [WARNING] [MemoryWorker] Memory Usage Reached Limit (525MB). Starting cleanup...
2026-08-28 15:06:31,626 [INFO] [System] Memory Cache Flushed. Process Stabilized.
```





### 프로세스 확인
```bash
pgrep -af agent-app-leak-x86
```

```text
3643 ./agent-app-leak-x86
3644 ./agent-app-leak-x86
```

### 초기 프로세스 메모리 사용량 확인
```bash
ps -C agent-app-leak-x86 -o pid,ppid,%cpu,%mem,rss,vsz,etime,cmd
```


```text
PID   PPID  %CPU  %MEM    RSS     VSZ     ELAPSED
3643  3592   0.1   0.0    2176    2904    00:54
3644  3643   2.1   2.7  454056  611040    00:54
```

### 이후 프로세스 메모리 사용량 확인
```bash
watch -n 3 "ps -C agent-app-leak-x86 -o pid,ppid,%cpu,%mem,rss,vsz,etime"
```

```text
PID   PPID  %CPU  %MEM    RSS     VSZ     ELAPSED
3643  3592   0.0   0.0    2020    2904    02:05
3644  3643   1.9   3.0  504960  765596    02:05
```


### Memory Leak 증거

```text
자식 프로세스 PID: 3644

RSS 초기값 : 454056 KB
RSS 이후값 : 504960 KB
증가량     : 50904 KB
```



### monitor.sh 시스템 상태 확인

```text
====== SYSTEM MONITOR RESULT ======
[HEALTH CHECK]
Checking process 'agent-app-leak-x86'... [OK] (PID: 3643)
Checking port 15034... [OK]
[FIREWALL CHECK]
UFW status... [OK]
CPU Usage : 4.8%
MEM Usage : 9.5%
DISK Used : 1%
[INFO] Log appended: /var/log/agent-app/monitor.log
```

### monitor.log 누적 기록 확인

```text
[2026-08-28 15:55:01] PID:3643 CPU:100.0% MEM:8.0% DISK_USED:1%
[2026-08-28 15:56:02] PID:3643 CPU:1.6% MEM:7.9% DISK_USED:1%
[2026-08-28 15:57:01] PID:3643 CPU:100.0% MEM:10.3% DISK_USED:1%
[2026-08-28 15:58:01] PID:3643 CPU:1.6% MEM:10.1% DISK_USED:1%
[2026-08-28 15:58:52] PID:3643 CPU:4.8% MEM:9.5% DISK_USED:1%
```


### After 결론

MEMORY_LIMIT을 256MB에서 512MB로 상향하면 프로세스의 조기 강제 종료를 방지하고 메모리 정리 후 안정화할 수 있지만, Memory Leak 자체가 제거된 것은 아니다. 
따라서 제한값 조정은 운영 안정성을 높이는 완화 조치이며, 근본적인 해결을 위해서는 메모리 증가 원인을 추가 분석해야 한다.
CPU_MAX_OCCUPY=50%와 MULTI_THREAD_ENABLE=False를 동일하게 유지하고 MEMORY_LIMIT만 256MB에서 512MB로 변경하여 비교하였다.

메모리 제한 상향 → 안정성 개선
Memory Leak 자체 → 여전히 존재
장애 영향은 줄였지만 근본 문제는 남아 있다