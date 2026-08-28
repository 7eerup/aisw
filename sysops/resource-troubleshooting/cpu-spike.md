## CPU 과점유 Case - Before


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
   ... MEMORY_LIMIT=512MB, CPU_MAX_OCCUPY=100%, MULTI_THREAD_ENABLE=False
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
2026-08-28 18:39:07,929 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-08-28 18:39:07,930 [INFO] Agent listening at port 15034

==================================================
 [ Agent Initiate ] Resource Check 
==================================================
 [ MEMORY ] Limit: 512MB 		[ OK ]
 [ CPU    ] Limit: 100%  		[ WARNING: Recommend Under 50% ]
 [ THREAD ] Concurrency: False 		[ OK ]
--------------------------------------------------
 >>> SYSTEM STATUS: STABLE. STARTING WORKLOAD MONITORING...
==================================================

2026-08-28 18:39:09,941 [INFO] [CpuWorker] Started. Maximum CPU Limit: 100%
2026-08-28 18:39:09,941 [INFO] [CpuWorker] Current Load: 5.00%
2026-08-28 18:39:13,049 [INFO] [CpuWorker] Current Load: 12.68%
2026-08-28 18:39:16,168 [INFO] [CpuWorker] Current Load: 21.84%
2026-08-28 18:39:19,289 [INFO] [CpuWorker] Current Load: 28.41%
2026-08-28 18:39:22,408 [INFO] [CpuWorker] Current Load: 29.94%
2026-08-28 18:39:25,527 [INFO] [CpuWorker] Current Load: 33.78%
2026-08-28 18:39:28,639 [INFO] [CpuWorker] Current Load: 39.04%
2026-08-28 18:39:31,759 [INFO] [CpuWorker] Current Load: 41.91%
2026-08-28 18:39:34,877 [INFO] [CpuWorker] Current Load: 43.43%
2026-08-28 18:39:37,996 [INFO] [CpuWorker] Current Load: 51.71%
2026-08-28 18:39:38,097 [CRITICAL] [CpuWorker] CPU Threshold Violated! (51.71%).

>>> [SYSTEM] WATCHDOG: INITIATING EMERGENCY ABORT (SIGTERM) <<<

Terminated
```


### 프로세스 PID 확인
```text
12309 ./agent-app-leak-x86
12310 ./agent-app-leak-x86
```


### top 프로세스 CPU 사용률 확인

```text
top - 18:39:35 up  4:34,  3 users,  load average: 0.03, 0.03, 0.00
Tasks:   1 total,   0 running,   1 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  1.3 ni, 98.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  16049.5 total,  15012.8 free,   1150.2 used,    114.7 buff/cache    
MiB Swap:  17073.5 total,  17073.5 free,      0.0 used.  14899.3 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND 
  12310 agent-a+  30  10   28308  18600  10136 S  10.0   0.1   0:00.30 agent-a+
```


### monitor.sh 시스템 CPU 상태 확인

```text
====== SYSTEM MONITOR RESULT ======
[HEALTH CHECK]
Checking process 'agent-app-leak-x86'... [OK] (PID: 12309)
Checking port 15034... [OK]
[FIREWALL CHECK]
UFW status... [OK]
CPU Usage : 100.0%
MEM Usage : 7.2%
DISK Used : 1%
[WARNING] CPU threshold exceeded (100.0% > 20%)
[INFO] Log appended: /var/log/agent-app/monitor.log




====== SYSTEM MONITOR RESULT ======
[HEALTH CHECK]
Checking process 'agent-app-leak-x86'... [OK] (PID: 12309)
Checking port 15034... [OK]
[FIREWALL CHECK]
UFW status... [OK]
CPU Usage : 100.0%
MEM Usage : 7.3%
DISK Used : 1%
[WARNING] CPU threshold exceeded (100.0% > 20%)
[INFO] Log appended: /var/log/agent-app/monitor.log
```

### monitor.log CPU 누적 기록 확인

```text
[2026-08-28 18:39:25] PID:12309 CPU:100.0% MEM:7.2% DISK_USED:1%
[2026-08-28 18:39:37] PID:12309 CPU:100.0% MEM:7.2% DISK_USED:1%
```



### CPU 과점유 Before 결론

`CPU_MAX_OCCUPY=100%`로 설정한 결과 `CpuWorker`의 부하가
`5.00% → 51.71%`까지 지속적으로 증가하였다.

애플리케이션 내부 보호 임계값인 50%를 초과하자
`CPU Threshold Violated`가 발생했으며,
Watchdog이 `SIGTERM`을 실행하여 프로세스가 종료되었다.

`top`을 통해 대상 자식 프로세스의 CPU 사용 상태를 확인했고,
`monitor.sh`와 `monitor.log`에서도 CPU 임계값 경고가 기록되었다.

따라서 높은 CPU 허용값으로 인해 CPU 과점유 상태가 발생하고,
Watchdog 보호 정책에 따라 프로세스가 종료되는 장애를 재현하였다.





## CPU 과점유 Case - After


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
2026-08-28 20:25:01,285 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-08-28 20:25:01,285 [INFO] Agent listening at port 15034

==================================================
 [ Agent Initiate ] Resource Check 
==================================================
 [ MEMORY ] Limit: 512MB 		[ OK ]
 [ CPU    ] Limit: 50%  		[ OK ]
 [ THREAD ] Concurrency: False 		[ OK ]
--------------------------------------------------
 >>> SYSTEM STATUS: STABLE. STARTING WORKLOAD MONITORING...
==================================================

2026-08-28 20:25:03,297 [INFO] >>> Scenario Selected: [Healthy System Monitoring]

>>> [SYSTEM] ALL CONFIGURATIONS OPTIMAL. RUNNING STABILITY TEST... <<<

2026-08-28 20:25:03,297 [INFO] [Scheduler] Task Scheduler Initialized.
2026-08-28 20:25:03,297 [INFO] [Scheduler] Registered Tasks: ['Thread-A', 'Thread-B', 'Thread-C']
2026-08-28 20:25:03,297 [INFO] [Scheduler] Starting task execution...
2026-08-28 20:25:03,298 [INFO] [Thread-B] Task Started. Calculating... (20%)
2026-08-28 20:25:03,349 [INFO] [Thread-B] Calculating... (40%)
2026-08-28 20:25:03,401 [INFO] [Thread-B] Calculating... (60%)
2026-08-28 20:25:03,453 [INFO] [Thread-B] Calculating... (80%)
2026-08-28 20:25:03,505 [INFO] [Thread-B] Task Completed. (100%)
2026-08-28 20:25:03,557 [INFO] [Thread-C] Task Started. Calculating... (20%)
2026-08-28 20:25:03,608 [INFO] [Thread-C] Calculating... (40%)
2026-08-28 20:25:03,660 [INFO] [Thread-C] Calculating... (60%)
2026-08-28 20:25:03,711 [INFO] [Thread-C] Calculating... (80%)
2026-08-28 20:25:03,763 [INFO] [Thread-C] Task Completed. (100%)
2026-08-28 20:25:03,815 [INFO] [Thread-A] Task Started. Calculating... (20%)
2026-08-28 20:25:03,867 [INFO] [Thread-A] Calculating... (40%)
2026-08-28 20:25:03,919 [INFO] [Thread-A] Calculating... (60%)
2026-08-28 20:25:03,970 [INFO] [Thread-A] Calculating... (80%)
2026-08-28 20:25:04,022 [INFO] [Thread-A] Task Completed. (100%)
2026-08-28 20:25:04,073 [INFO] [Scheduler] All tasks completed.
2026-08-28 20:25:04,109 [INFO] [MemoryWorker] Current Heap: 25MB
2026-08-28 20:25:04,110 [INFO] [CpuWorker] Started. Maximum CPU Limit: 50%
2026-08-28 20:25:04,110 [INFO] [CpuWorker] Current Load: 5.00%
2026-08-28 20:25:07,165 [INFO] [MemoryWorker] Current Heap: 50MB
2026-08-28 20:25:07,230 [INFO] [CpuWorker] Current Load: 6.61%
2026-08-28 20:25:10,219 [INFO] [MemoryWorker] Current Heap: 75MB
2026-08-28 20:25:10,351 [INFO] [CpuWorker] Current Load: 6.96%
2026-08-28 20:25:13,274 [INFO] [MemoryWorker] Current Heap: 100MB
2026-08-28 20:25:13,469 [INFO] [CpuWorker] Current Load: 10.84%
2026-08-28 20:25:16,328 [INFO] [MemoryWorker] Current Heap: 125MB
2026-08-28 20:25:16,588 [INFO] [CpuWorker] Current Load: 16.77%
2026-08-28 20:25:19,383 [INFO] [MemoryWorker] Current Heap: 150MB
2026-08-28 20:25:19,709 [INFO] [CpuWorker] Current Load: 17.26%
2026-08-28 20:25:22,437 [INFO] [MemoryWorker] Current Heap: 175MB
2026-08-28 20:25:22,827 [INFO] [CpuWorker] Current Load: 19.76%
2026-08-28 20:25:25,489 [INFO] [MemoryWorker] Current Heap: 200MB
2026-08-28 20:25:25,947 [INFO] [CpuWorker] Current Load: 23.94%
2026-08-28 20:25:28,536 [INFO] [MemoryWorker] Current Heap: 225MB
2026-08-28 20:25:29,066 [INFO] [CpuWorker] Current Load: 24.12%
2026-08-28 20:25:31,591 [INFO] [MemoryWorker] Current Heap: 250MB
2026-08-28 20:25:32,186 [INFO] [CpuWorker] Current Load: 32.19%
2026-08-28 20:25:34,645 [INFO] [MemoryWorker] Current Heap: 275MB
2026-08-28 20:25:35,306 [INFO] [CpuWorker] Current Load: 36.82%
2026-08-28 20:25:37,699 [INFO] [MemoryWorker] Current Heap: 300MB
2026-08-28 20:25:38,427 [INFO] [CpuWorker] Current Load: 38.78%
2026-08-28 20:25:40,753 [INFO] [MemoryWorker] Current Heap: 325MB
2026-08-28 20:25:41,547 [INFO] [CpuWorker] Current Load: 45.17%
2026-08-28 20:25:43,807 [INFO] [MemoryWorker] Current Heap: 350MB
2026-08-28 20:25:44,667 [INFO] [CpuWorker] Current Load: 49.42%
2026-08-28 20:25:46,780 [INFO] [CpuWorker] Peak reached (50.00%). Starting cooldown...
2026-08-28 20:25:46,859 [INFO] [MemoryWorker] Current Heap: 375MB
2026-08-28 20:25:47,783 [INFO] [CpuWorker] Current Load: 50.00%
2026-08-28 20:25:49,915 [INFO] [MemoryWorker] Current Heap: 400MB
2026-08-28 20:25:50,921 [INFO] [CpuWorker] Current Load: 47.25%
2026-08-28 20:25:52,969 [INFO] [MemoryWorker] Current Heap: 425MB
2026-08-28 20:25:54,039 [INFO] [CpuWorker] Current Load: 40.26%
2026-08-28 20:25:56,021 [INFO] [MemoryWorker] Current Heap: 450MB
2026-08-28 20:25:57,159 [INFO] [CpuWorker] Current Load: 31.77%
2026-08-28 20:25:59,075 [INFO] [MemoryWorker] Current Heap: 475MB
2026-08-28 20:26:00,276 [INFO] [CpuWorker] Current Load: 29.72%
2026-08-28 20:26:02,130 [INFO] [MemoryWorker] Current Heap: 500MB
2026-08-28 20:26:03,396 [INFO] [CpuWorker] Current Load: 24.10%
2026-08-28 20:26:05,186 [INFO] [MemoryWorker] Current Heap: 525MB
2026-08-28 20:26:05,186 [WARNING] [MemoryWorker] Memory Usage Reached Limit (525MB). Starting cleanup...
2026-08-28 20:26:05,195 [INFO] [System] Memory Cache Flushed. Process Stabilized.
```



### 프로세스 PID 확인

```bash
pgrep -af agent-app-leak-x86
```

```text
13314 ./agent-app-leak-x86
13315 ./agent-app-leak-x86
```

### 프로세스 CPU·메모리 상태 실시간 확인

```bash
watch -n 1 "ps -C agent-app-leak-x86 -o pid,ppid,%cpu,%mem,etime,stat,cmd"
```


```text
Every 1.0s: ps -C agent-app-leak-x86 -o pid...  ubuntu: Fri Aug 28 20:25:42 2026

PID    PPID %CPU %MEM     ELAPSED STAT CMD
13314   13304  0.1  0.0       00:40 S+   ./agent-app-leak-x86
13315   13314  2.0  2.1       00:40 SNl+ ./agent-app-leak-x86
```




### monitor.sh 시스템 상태 확인

```bash
sudo -u agent-admin /home/agent-admin/agent-app/bin/monitor.sh
```

### monitor.log CPU·메모리 누적 기록 확인

```bash
sudo tail -n 5 /var/log/agent-app/monitor.log
```


```text
====== SYSTEM MONITOR RESULT ======

[HEALTH CHECK]

Checking process 'agent-app-leak-x86'... [OK] (PID: 13314)

Checking port 15034... [OK]

[FIREWALL CHECK]

UFW status... [OK]
CPU Usage : 100.0%
MEM Usage : 10.5%
DISK Used : 1%

[WARNING] CPU threshold exceeded (100.0% > 20%)
[WARNING] MEM threshold exceeded (10.5% > 10%)

[INFO] Log appended: /var/log/agent-app/monitor.log
```



```
[2026-08-28 20:25:02] PID:13314 CPU:100.0% MEM:7.7% DISK_USED:1%
[2026-08-28 20:25:55] PID:13314 CPU:100.0% MEM:10.5% DISK_USED:1%
```


### CPU 과점유 After 결론

`CPU_MAX_OCCUPY`를 `100% → 50%`로 낮춘 결과,
`CpuWorker`의 부하가 50%에 도달했을 때 `Peak reached`가 발생하고
자동으로 cooldown이 수행되었다.

CPU 부하는 이후 `47.25% → 40.26% → 31.77% → 24.10%`로 감소했으며,
`CPU Threshold Violated`, `WATCHDOG`, `SIGTERM`은 발생하지 않았다.

또한 프로세스가 계속 실행되는 것을 확인하였다.

따라서 `CPU_MAX_OCCUPY`를 50%로 제한함으로써
CPU 과점유에 따른 Watchdog 강제 종료를 방지하고
프로세스 안정성을 개선할 수 있었다.