## Deadlock Case - Before



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
   ... MEMORY_LIMIT=512MB, CPU_MAX_OCCUPY=50%, MULTI_THREAD_ENABLE=True
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
2026-08-28 21:25:50,420 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-08-28 21:25:50,421 [INFO] Agent listening at port 15034

==================================================
 [ Agent Initiate ] Resource Check 
==================================================
 [ MEMORY ] Limit: 512MB 		[ OK ]
 [ CPU    ] Limit: 50%  		[ OK ]
 [ THREAD ] Concurrency: True 		[ WARNING ]
--------------------------------------------------
 >>> SYSTEM WARNING: POTENTIAL DEADLOCK IN CONCURRENT MODE.
==================================================

2026-08-28 21:25:52,432 [WARNING] [AgentWorker] Initializing concurrent transaction processors...
2026-08-28 21:25:52,432 [WARNING] [System] CAUTION: Strict resource locking is enabled.
2026-08-28 21:25:57,460 [INFO] [Worker-Thread-1] Process Started. Attempting to lock [Shared_Memory_A]...
2026-08-28 21:25:57,461 [INFO] [AgentWorker][Worker-Thread-1] LOCK ACQUIRED: [Shared_Memory_A]. (Holding...)
2026-08-28 21:25:57,461 [INFO] [AgentWorker][Worker-Thread-1] Processing critical data in Memory A...
2026-08-28 21:25:57,461 [INFO] [AgentWorker][Worker-Thread-2] Process Started. Attempting to lock [Socket_Pool_B]...
2026-08-28 21:25:57,462 [INFO] [AgentWorker][Worker-Thread-2] LOCK ACQUIRED: [Socket_Pool_B]. (Holding...)
2026-08-28 21:25:57,462 [INFO] [AgentWorker][Worker-Thread-2] Establishing network connections in Pool B...
2026-08-28 21:25:57,463 [INFO] [AgentWorker] Waiting for worker threads to complete transactions...
2026-08-28 21:25:59,474 [INFO] [AgentWorker][Worker-Thread-1] Need resource [Socket_Pool_B] to finish job.
2026-08-28 21:25:59,474 [INFO] [AgentWorker][Worker-Thread-1] WAITING for [Socket_Pool_B]... (Status: BLOCKED)
2026-08-28 21:25:59,475 [INFO] [AgentWorker][Worker-Thread-2] Need resource [Shared_Memory_A] to write logs.
2026-08-28 21:25:59,475 [INFO] [AgentWorker][Worker-Thread-2] WAITING for [Shared_Memory_A]... (Status: BLOCKED)
```





### 프로세스 PID 확인

```bash
pgrep -af agent-app-leak-x86
```

### 프로세스 생존 확인

```text
25710 ./agent-app-leak-x86
25711 ./agent-app-leak-x86
```

### 프로세스 생존 및 CPU·메모리 상태 확인

```bash
ps -C agent-app-leak-x86 -o pid,ppid,%cpu,%mem,etime,stat,cmd
```

```text
    PID    PPID %CPU %MEM     ELAPSED STAT CMD

  25710   25622  0.0  0.0       09:19 S+   ./agent-app-leak-x86
  25711   25710  0.0  0.1       09:19 SNl+ ./agent-app-leak-x86
```


### 자식 프로세스 PID 지정

```bash
PID=$(pgrep -n -f agent-app-leak-x86); echo $PID
```


### ps -L 스레드 상태 확인

```bash
ps -L -p $PID -o pid,ppid,lwp,psr,pcpu,pmem,stat,etime,comm
```

```text
    PID    PPID     LWP PSR %CPU %MEM STAT     ELAPSED COMMAND

  25711   25710   25711   4  0.0  0.1 SNl+       09:33 agent-app-leak-

  25711   25710   25733   2  0.0  0.1 SNl+       09:26 agent-app-leak-

  25711   25710   25734   1  0.0  0.1 SNl+       09:26 agent-app-leak-
```


### top -H 스레드 상태 확인

```bash
top -H -p $PID
```

```text
top - 21:35:45 up  7:30,  3 users,  load average: 0.00, 0.01, 0.00

Threads: **  3** total, **  0** running, **  3** sleeping, **  0** stopped, **  0** zombie

%Cpu(s):**  0.0** us,**  0.0** sy,**  0.0** ni,100.0 id,**  0.0** wa,**  0.0** hi,**  0.0** si,**  0.0** st

MiB Mem :**  16049.5** total,**  14827.1** free, **  1307.0** used,**    172.6** buff/cache    

MiB Swap:**  17073.5** total,**  17073.5** free,**      0.0** used.**  14742.5** avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND 

  25711 agent-a+  30  10  175772  17592   9120 S   0.0   0.1   0:00.05 agent-a+

  25733 agent-a+  30  10  175772  17592   9120 S   0.0   0.1   0:00.00 agent-a+

  25734 agent-a+  30  10  175772  17592   9120 S   0.0   0.1   0:00.00 agent-a+
```


### Deadlock Before 결론

`MULTI_THREAD_ENABLE=True`로 설정한 결과,
`Worker-Thread-1`과 `Worker-Thread-2`가 각각 서로 다른 자원을 획득한 후
상대 스레드가 보유한 자원을 기다리며 `WAITING / BLOCKED` 상태에 진입하였다.

프로세스는 9분 이상 종료되지 않고 유지되었지만,
`ps -L`과 `top -H`에서 3개 스레드 모두 CPU 사용률이 `0.0%`이고
sleeping 상태로 유지되는 것을 확인하였다.

따라서 프로세스는 살아 있지만 스레드 간 상호 자원 대기로
작업이 진행되지 않는 Deadlock 상태가 발생한 것을 확인하였다.





## Deadlock Case - After


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
2026-08-28 22:03:39,071 [INFO] [SafetyGuard] Process priority lowered (nice=10).
2026-08-28 22:03:39,071 [INFO] Agent listening at port 15034

==================================================
 [ Agent Initiate ] Resource Check 
==================================================
 [ MEMORY ] Limit: 512MB 		[ OK ]
 [ CPU    ] Limit: 50%  		[ OK ]
 [ THREAD ] Concurrency: False 		[ OK ]
--------------------------------------------------
 >>> SYSTEM STATUS: STABLE. STARTING WORKLOAD MONITORING...
==================================================

2026-08-28 22:03:41,083 [INFO] >>> Scenario Selected: [Healthy System Monitoring]

>>> [SYSTEM] ALL CONFIGURATIONS OPTIMAL. RUNNING STABILITY TEST... <<<

2026-08-28 22:03:41,084 [INFO] [Scheduler] Task Scheduler Initialized.
2026-08-28 22:03:41,084 [INFO] [Scheduler] Registered Tasks: ['Thread-A', 'Thread-B', 'Thread-C']
2026-08-28 22:03:41,084 [INFO] [Scheduler] Starting task execution...
2026-08-28 22:03:41,084 [INFO] [Thread-B] Task Started. Calculating... (20%)
2026-08-28 22:03:41,136 [INFO] [Thread-B] Calculating... (40%)
2026-08-28 22:03:41,187 [INFO] [Thread-B] Calculating... (60%)
2026-08-28 22:03:41,238 [INFO] [Thread-B] Calculating... (80%)
2026-08-28 22:03:41,290 [INFO] [Thread-B] Task Completed. (100%)
2026-08-28 22:03:41,341 [INFO] [Thread-C] Task Started. Calculating... (20%)
2026-08-28 22:03:41,393 [INFO] [Thread-C] Calculating... (40%)
2026-08-28 22:03:41,445 [INFO] [Thread-C] Calculating... (60%)
2026-08-28 22:03:41,496 [INFO] [Thread-C] Calculating... (80%)
2026-08-28 22:03:41,546 [INFO] [Thread-C] Task Completed. (100%)
2026-08-28 22:03:41,598 [INFO] [Thread-A] Task Started. Calculating... (20%)
2026-08-28 22:03:41,650 [INFO] [Thread-A] Calculating... (40%)
2026-08-28 22:03:41,702 [INFO] [Thread-A] Calculating... (60%)
2026-08-28 22:03:41,753 [INFO] [Thread-A] Calculating... (80%)
2026-08-28 22:03:41,804 [INFO] [Thread-A] Task Completed. (100%)
2026-08-28 22:03:41,856 [INFO] [Scheduler] All tasks completed.
2026-08-28 22:03:41,892 [INFO] [MemoryWorker] Current Heap: 25MB
2026-08-28 22:03:41,892 [INFO] [CpuWorker] Started. Maximum CPU Limit: 50%
2026-08-28 22:03:41,893 [INFO] [CpuWorker] Current Load: 5.00%
2026-08-28 22:03:44,948 [INFO] [MemoryWorker] Current Heap: 50MB
2026-08-28 22:03:45,014 [INFO] [CpuWorker] Current Load: 12.77%
2026-08-28 22:03:48,005 [INFO] [MemoryWorker] Current Heap: 75MB
2026-08-28 22:03:48,133 [INFO] [CpuWorker] Current Load: 13.52%
2026-08-28 22:03:51,054 [INFO] [MemoryWorker] Current Heap: 100MB
2026-08-28 22:03:51,251 [INFO] [CpuWorker] Current Load: 15.64%
2026-08-28 22:03:54,101 [INFO] [MemoryWorker] Current Heap: 125MB
2026-08-28 22:03:54,371 [INFO] [CpuWorker] Current Load: 23.95%
2026-08-28 22:03:57,155 [INFO] [MemoryWorker] Current Heap: 150MB
2026-08-28 22:03:57,490 [INFO] [CpuWorker] Current Load: 32.92%
2026-08-28 22:04:00,208 [INFO] [MemoryWorker] Current Heap: 175MB
2026-08-28 22:04:00,609 [INFO] [CpuWorker] Current Load: 37.84%
2026-08-28 22:04:03,262 [INFO] [MemoryWorker] Current Heap: 200MB
2026-08-28 22:04:03,728 [INFO] [CpuWorker] Current Load: 44.92%
2026-08-28 22:04:06,319 [INFO] [MemoryWorker] Current Heap: 225MB
2026-08-28 22:04:06,846 [INFO] [CpuWorker] Current Load: 49.15%
2026-08-28 22:04:08,960 [INFO] [CpuWorker] Peak reached (50.00%). Starting cooldown...
2026-08-28 22:04:09,374 [INFO] [MemoryWorker] Current Heap: 250MB
2026-08-28 22:04:09,966 [INFO] [CpuWorker] Current Load: 50.00%
2026-08-28 22:04:12,430 [INFO] [MemoryWorker] Current Heap: 275MB
2026-08-28 22:04:13,085 [INFO] [CpuWorker] Current Load: 45.75%
2026-08-28 22:04:15,486 [INFO] [MemoryWorker] Current Heap: 300MB
2026-08-28 22:04:16,204 [INFO] [CpuWorker] Current Load: 38.57%
2026-08-28 22:04:18,542 [INFO] [MemoryWorker] Current Heap: 325MB
2026-08-28 22:04:19,322 [INFO] [CpuWorker] Current Load: 29.68%
2026-08-28 22:04:21,598 [INFO] [MemoryWorker] Current Heap: 350MB
2026-08-28 22:04:22,441 [INFO] [CpuWorker] Current Load: 24.09%
2026-08-28 22:04:24,644 [INFO] [MemoryWorker] Current Heap: 375MB
2026-08-28 22:04:25,561 [INFO] [CpuWorker] Current Load: 23.75%
2026-08-28 22:04:27,701 [INFO] [MemoryWorker] Current Heap: 400MB
2026-08-28 22:04:28,707 [INFO] [CpuWorker] Current Load: 20.65%
2026-08-28 22:04:30,757 [INFO] [MemoryWorker] Current Heap: 425MB
2026-08-28 22:04:31,824 [INFO] [CpuWorker] Current Load: 20.42%
2026-08-28 22:04:33,800 [INFO] [MemoryWorker] Current Heap: 450MB
2026-08-28 22:04:34,944 [INFO] [CpuWorker] Current Load: 16.83%
2026-08-28 22:04:36,856 [INFO] [MemoryWorker] Current Heap: 475MB
2026-08-28 22:04:38,062 [INFO] [CpuWorker] Current Load: 16.29%
2026-08-28 22:04:39,910 [INFO] [MemoryWorker] Current Heap: 500MB
2026-08-28 22:04:41,179 [INFO] [CpuWorker] Current Load: 8.46%
2026-08-28 22:04:42,966 [INFO] [MemoryWorker] Current Heap: 525MB
2026-08-28 22:04:42,966 [WARNING] [MemoryWorker] Memory Usage Reached Limit (525MB). Starting cleanup...
2026-08-28 22:04:42,975 [INFO] [System] Memory Cache Flushed. Process Stabilized.

>>> [SYSTEM] MEMORY RECOVERED (Cache Cleared) <<<
```

### 프로세스 PID 확인

```bash
pgrep -af agent-app-leak-x86
```

```text
27022 ./agent-app-leak-x86
27023 ./agent-app-leak-x86
```


### 자식 프로세스 스레드 상태 확인

```bash
PID=$(pgrep -n -f agent-app-leak-x86); ps -L -p $PID -o pid,ppid,lwp,psr,pcpu,pmem,stat,etime,comm
```

```text
    PID    PPID     LWP PSR %CPU %MEM STAT     ELAPSED COMMAND
  27023   27022   27023   4  0.1  2.2 SNl+       00:44 agent-app-leak-
  27023   27022   27024   5  1.2  2.2 SNl+       00:41 agent-app-leak-
  27023   27022   27025   0  1.0  2.2 SNl+       00:41 agent-app-leak-
```

### top -H 스레드 실행 상태 확인

```bash
top -H -p $PID
```

```text
top - 22:04:36 up  7:59,  3 users,  load average: 0.00, 0.00, 0.00
Threads:   3 total,   1 running,   2 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.1 us,  0.1 sy,  0.1 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  16049.5 total,  14470.5 free,   1711.5 used,     76.6 buff/cache    
MiB Swap:  17073.5 total,  17073.5 free,      0.0 used.  14338.0 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND 
  27024 agent-a+  30  10  662248 487676   9952 R   0.7   3.0   0:00.67 agent-a+
  27025 agent-a+  30  10  662248 487692   9952 S   0.7   3.0   0:00.51 agent-a+
  27023 agent-a+  30  10  662248 487676   9952 S   0.0   3.0   0:00.05 agent-a+
```



### Deadlock After 결론

`MULTI_THREAD_ENABLE`을 `True → False`로 변경한 결과,
Before에서 발생했던 스레드 간 상호 자원 대기와 `WAITING / BLOCKED` 상태가 발생하지 않았다.

`Thread-B`, `Thread-C`, `Thread-A`가 순차적으로 작업을 완료했고,
`Scheduler`에서도 `All tasks completed`가 확인되었다.

또한 `ps -L`과 `top -H`를 통해 스레드가 정상적으로 동작하고 있음을 확인하였다.

따라서 멀티스레드 동시 실행을 비활성화함으로써 Deadlock을 방지하고 작업을 정상적으로 완료할 수 있었다.