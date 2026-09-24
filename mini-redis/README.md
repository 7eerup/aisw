# Mini Redis

## Data Structure and Algorithm

* 자료구조 = 데이터를 저장하고 관리하는 방법
* 알고리즘 = 데이터를 사용하여 문제를 해결하는 절차

| 구분        | 분류      | 역할                   |
| --------- | ------- | -------------------- |
| 이중 연결 리스트 | 자료구조    | LRU 사용 순서 관리         |
| 해시맵       | 자료구조    | 키-값 저장 및 빠른 조회       |
| 최소 힙      | 자료구조    | 가장 빠른 만료 데이터 확인      |
| LRU       | 알고리즘/정책 | 가장 오래 사용하지 않은 데이터 제거 |


## LRU (Least Recently Used)

가장 오래 사용하지 않은 데이터를 우선적으로 제거하는 방식

이중 연결 리스트의 `tail`이 가장 오래 사용하지 않은 키를 가리키도록 관리하여, 전체 데이터를 순회하지 않고 제거 대상을 확인할 수 있습니다.

## 프로젝트 구조

```text
mini-redis/
├── README.md
├── main.py
├── mini_redis.py
└── structures/
    ├── __init__.py
    ├── doubly_linked_list.py
    ├── hash_map.py
    └── min_heap.py
```



### 파일별 역할

* `main.py`

  * CLI 진입점
  * 사용자 명령어 입력, 파싱 및 검증
  * 실행 결과와 에러 메시지 출력

| 명령                       | 기능          | 호출 메서드                  |
| ------------------------ | ----------- | ----------------------- |
| `SET key value`          | 데이터 저장      | `redis.set()`           |
| `GET key`                | 데이터 조회      | `redis.get()`           |
| `DEL key`                | 데이터 삭제      | `redis.delete()`        |
| `EXISTS key`             | 키 존재 확인     | `redis.exists()`        |
| `DBSIZE`                 | 키 개수 조회     | `redis.dbsize()`        |
| `KEYS`                   | 모든 키 조회     | `redis.keys()`          |
| `EXPIRE key seconds`     | 만료 시간 설정    | `redis.expire()`        |
| `TTL key`                | 남은 만료 시간 조회 | `redis.ttl()`           |
| `CONFIG SET maxmemory n` | 최대 메모리 설정   | `redis.set_maxmemory()` |
| `INFO memory`            | 메모리 정보 조회   | `redis.info_memory()`   |
| `exit`, `quit`           | CLI 종료      | 해당 없음                   |



* `mini_redis.py`

  * store + HashMap: 빠른 데이터 저장과 조회
  * lru_list + lru_nodes: 가장 오래 사용하지 않은 키를 빠르게 제거
  * expiry_heap + expirations: 가장 빠르게 만료되는 키를 효율적으로 정리
  * Mini Redis의 핵심 동작 담당
  * SET, GET, DEL, EXISTS, DBSIZE, KEYS 구현
  * LRU 및 메모리 제한 관리
  * EXPIRE, TTL을 통한 만료 관리


* `structures/hash_map.py`

  * key-value 데이터 저장 및 조회
  * 사용자 정의 해시 함수
  * 체이닝 방식 충돌 처리
  * 로드 팩터에 따른 버킷 확장

* `structures/doubly_linked_list.py`

  * LRU 사용 순서 관리
  * 최근 사용 키를 `head` 방향으로 관리
  * 가장 오래 사용하지 않은 키를 `tail`에서 제거

* `structures/min_heap.py`

  * TTL 만료 순서 관리
  * `(expire_at, key)` 형태의 데이터 저장
  * 가장 빠른 만료 시간 확인



  ## 테스트

### String 타입 기본 동작 테스트

```text
mini-redis> SET name Alice
OK

mini-redis> GET name
"Alice"

mini-redis> EXISTS name
(integer) 1

mini-redis> DBSIZE
(integer) 1

mini-redis> KEYS
1) "name"

mini-redis> DEL name
(integer) 1

mini-redis> GET name
(nil)

mini-redis> EXISTS name
(integer) 0

mini-redis> DBSIZE
(integer) 0

mini-redis> KEYS
(empty array)
```

### LRU 자동 제거 테스트

```text
mini-redis> CONFIG SET maxmemory 10
OK

mini-redis> SET a 1111
OK

mini-redis> SET b 2222
OK

mini-redis> GET a
"1111"

mini-redis> SET c 3333
OK

# 결과

mini-redis> GET a
"1111"

mini-redis> GET b
(nil)

mini-redis> GET c
"3333"

mini-redis> DBSIZE
(integer) 2
```

key 1바이트 + value 4바이트 = 데이터당 5바이트

```text
SET a 1111 → used_memory 5 bytes
SET b 2222 → used_memory 10 bytes
GET a      → a를 최근 사용 데이터로 갱신
SET c 3333 → 메모리 제한 초과
```

LRU 정책에 따라 가장 오래 사용하지 않은 `b` 삭제

```text
a(유지) / b(삭제) / c(유지)
```

### INFO memory 테스트

`evicted_keys`는 메모리 제한 때문에 LRU 정책으로 자동 제거된 키의 누적 개수

```text
mini-redis> INFO memory
used_memory:10
maxmemory:10
evicted_keys:1
```

### EXPIRE / TTL 테스트

```text
mini-redis> SET temp hello
OK

mini-redis> EXPIRE temp 10
(integer) 1

mini-redis> TTL temp
(integer) 5

mini-redis> GET temp
"hello"

mini-redis> TTL temp
(integer) -2

mini-redis> GET temp
(nil)
```

TTL 값은 명령 실행 시점에 따라 달라질 수 있으며, 만료된 키는 삭제되고 TTL 조회 시 `-2`를 반환

### 에러 처리 테스트

```text
mini-redis> HELLO
(error) ERR unknown command 'HELLO'

mini-redis> GET
(error) ERR wrong number of arguments for 'GET' command

mini-redis> SET key
(error) ERR wrong number of arguments for 'SET' command

mini-redis> EXPIRE key abc
(error) ERR value is not an integer or out of range

mini-redis> CONFIG SET maxmemory abc
(error) ERR value is not an integer or out of range
```

### Out Of Memory

```text
mini-redis> CONFIG SET maxmemory 3
OK

mini-redis> SET a 1111
(error) OOM command not allowed when used_memory > 'maxmemory'
```