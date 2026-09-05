# [Analysis] 로그 패턴을 통한 스케줄링 알고리즘 추론

## 1. 테스트 환경


| 환경 변수                 |     설정값 | 의미          |
| --------------------- | ------: | ----------- |
| `MEMORY_LIMIT`        | `512MB` | 메모리 사용 제한   |
| `CPU_MAX_OCCUPY`      |   `50%` | 최대 CPU 사용률  |
| `MULTI_THREAD_ENABLE` | `false` | 멀티스레드 기능 설정 |

## 2. 실행 및 로그 수집

애플리케이션을 실행하면서 출력 로그를 `scheduling-test.log` 파일에 저장하였다.

```bash
cd ~/agent-app
./agent-app-leak-x86 2>&1 | tee scheduling-test.log
```

이후 `Scheduler`와 `Thread-A`, `Thread-B`, `Thread-C` 관련 로그만 추출하였다.

```bash
grep -nE 'Thread-[ABC]|Scheduler' ~/agent-app/scheduling-test.log
```

## 3. 관찰 결과

Scheduler는 `Thread-A`, `Thread-B`, `Thread-C`를 등록한 후 다음 순서로 작업을 실행하였다.

```text
Thread-A : 20% → 40% → Preempted
Thread-B : 20% → 40% → Preempted
Thread-C : 20% → 40% → Preempted

Thread-A : 60% → 80% → Preempted
Thread-B : 60% → 80% → Preempted
Thread-C : 60% → 80% → Preempted

Thread-A : 100%
Thread-B : 100%
Thread-C : 100%
```

모든 작업이 완료된 후 Scheduler는 다음 메시지를 출력하였다.

```text
All tasks completed
```

## 4. 실행 패턴 분석

전체 실행 순서는 다음과 같다.

```text
A → B → C → A → B → C → A → B → C
```

각 Thread는 작업이 끝날 때까지 계속 실행되지 않았다.

일정 구간까지 실행된 후 `Preempted` 되었고, 다른 Thread가 실행된 뒤 자신의 차례가 돌아오면 이전 진행 상태에서 다시 실행되었다.

즉, 여러 Thread가 실행 기회를 순서대로 나누어 사용한 형태이다.

## 5. 알고리즘 추론

이 실행 패턴은 **Round-Robin 스케줄링 방식과 가장 유사하다.**

근거는 다음과 같다.

* 하나의 Thread가 작업 완료까지 실행 기회를 독점하지 않는다.
* `Thread-A → Thread-B → Thread-C` 순서가 반복된다.
* 실행 중인 Thread가 `Preempted` 되어 다른 Thread로 전환된다.
* 다시 실행될 때 이전 진행 상태에서 작업을 계속한다.
* 각 Thread가 비교적 균등하게 실행 기회를 받는다.

따라서 하나의 작업을 먼저 끝까지 처리하는 **FCFS** 방식이나 우선순위에 따라 실행 순서가 결정되는 **Priority Scheduling** 방식보다 **Round-Robin** 방식에 가깝다고 판단하였다.

## 6. 결론

로그에서 확인된

```text
A → B → C → A → B → C → A → B → C
```

실행 순서와 `Preempted` 패턴을 근거로, 애플리케이션 내부 Task Scheduler는 **Round-Robin과 유사한 방식으로 작업을 처리하는 것으로 추론하였다.**
