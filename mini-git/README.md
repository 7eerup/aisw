# Mini Git

## 자료구조 및 알고리즘 핵심 개념

### 시간복잡도(Big O)

데이터 크기에 따라 알고리즘의 작업량이 어떻게 증가하는지 나타내는 표기법

- **O(1) — 상수 시간:** 데이터 크기와 관계없이 작업량이 일정한 수준
- **O(n) — 선형 시간:** 데이터 크기에 비례하여 작업량 증가
- **O(n log n) — 선형 로그 시간:** 데이터를 반복적으로 분할하고 병합
- **O(V + E) — 그래프 탐색:** 노드와 간선 수에 비례하여 작업량 증가

**시간복잡도 표기**
- `n`: 데이터 수
- `V`: 노드(Vertex), 즉 커밋 수
- `E`: 간선(Edge), 즉 부모·자식 연결 수

### Mini Git 주요 알고리즘 시간복잡도

| 알고리즘 | 활용 명령어 | 시간복잡도 | 핵심 이유 |
|---|---|---|---|
| 위상 정렬(Kahn) | `LOG` | O(V + E) | 모든 커밋과 부모 관계를 처리 |
| 병합 정렬(Merge Sort) | `LOG --sort-by=date`, `LOG --sort-by=author` | O(n log n) | 절반씩 분할하고 단계마다 병합 |
| BFS(너비 우선 탐색) | `PATH` | O(V + E) | Queue로 노드와 간선을 탐색 |
| DFS(깊이 우선 탐색) | `ANCESTORS` | O(V + E) | Stack으로 조상과 부모 관계를 탐색 |

**자료구조 활용**
- **O(1):** Dictionary에서 커밋 해시(Key)로 객체 조회 — 평균 시간복잡도
- **O(n):** List에서 특정 커밋을 순차 검색 — 최악 시간복잡도

※ 시간복잡도는 각 알고리즘의 기본 연산 기준입니다. 실제 `PATH`에는 경로 복원이, `LOG --sort-by`에는 병합 정렬 이전의 위상 정렬이 추가됩니다.


### 위상 정렬(Topological Sort)

방향 비순환 그래프(DAG)에서 부모 노드가 자식 노드보다 먼저 나오도록 정렬하는 알고리즘

- **탐색 방식:** Queue와 부모 개수를 활용
- **특징:** 부모 커밋을 자식 커밋보다 먼저 출력
- **활용:** `LOG` 명령어로 커밋 이력 정렬

### Queue(큐)

먼저 들어온 데이터를 먼저 처리하는 FIFO(First In, First Out) 방식의 자료구조

- `append()`: 데이터 추가
- `popleft()`: 가장 먼저 들어온 데이터 추출 및 제거
- **활용:** Kahn 위상 정렬, BFS

### BFS(너비 우선 탐색)

그래프에서 가까운 노드부터 차례대로 탐색하는 알고리즘

- **탐색 방식:** Queue를 활용하여 가까운 노드부터 탐색
- **특징:** 가중치가 없는 그래프에서 최단 경로 탐색 가능
- **활용:** `PATH` 명령어로 두 커밋 사이의 최단 경로 탐색

### Graph(그래프)

노드(Node)와 간선(Edge)으로 데이터 간의 연결 관계를 표현하는 자료구조

- **Node:** 개별 커밋
- **Edge:** 커밋 사이의 부모·자식 관계
- **DAG:** 사이클이 없는 방향 그래프로 커밋 이력 관리
- **활용:** `LOG` 위상 정렬, `PATH` 최단 경로, `ANCESTORS` 조상 탐색

### Stack(스택)

마지막에 들어온 데이터를 먼저 처리하는 LIFO(Last In, First Out) 방식의 자료구조

- `append()`: 데이터 추가
- `pop()`: 마지막에 들어온 데이터 추출 및 제거
- **활용:** DFS

### 병합 정렬(Merge Sort)

리스트를 재귀적으로 절반씩 분할하고, 원소가 1개 이하가 되면 정렬된 부분 리스트를 비교·병합하는 알고리즘입니다.

- **핵심:** 분할 → 재귀 호출 → 비교·병합
- **활용:** 날짜·작성자 기준 오름차순 정렬

### 커밋 그래프(DAG)

- **Directed(방향성):** 자식 커밋이 부모 커밋을 참조합니다.
- **Acyclic(비순환):** 부모 참조를 따라 이동해도 순환이 발생하지 않습니다.
- **Graph(그래프):** 커밋 노드와 부모 참조 간선으로 구성됩니다.

```
# 커밋 그래프(DAG) 정의
커밋 간 부모·자식 관계를 나타낸 관계도가 바로 커밋 그래프(Commit Graph)의 시각적 표현

# 노드(Node)
Commit 객체가 하나의 데이터를 나타내므로 커밋 하나를 노드 하나로 표현

000002 ───────→ 000001
  │                │
  │                └── 부모 커밋 (Node)
  │
  └── 자식 커밋 (Node)

화살표 ───────→ : 부모 참조 관계 (Edge)
```


### Mini Git 알고리즘 요약

| 알고리즘 | 주요 자료구조 | 실행 명령어 |
|---|---|---|
| Kahn 위상 정렬 | Queue | `LOG` |
| 병합 정렬 | List, 재귀 호출 | `LOG --sort-by=date`, `LOG --sort-by=author` |
| DFS | Stack | `ANCESTORS` |
| BFS | Queue | `PATH` |
| 역색인 검색 | Dictionary, Set | `SEARCH` |


## Python collections 주요 자료구조

| 자료구조 | 역할 | 활용 예시 |
|---|---|---|
| `deque` | 양쪽 끝에서 빠르게 추가·삭제 | Queue, Stack, BFS |
| `Counter` | 요소별 등장 횟수 계산 | 단어 빈도 분석 |
| `defaultdict` | 없는 키에 기본값 자동 생성 | 그래프 인접 리스트 |
| `OrderedDict` | 삽입 순서를 관리하고 순서 변경 지원 | LRU 캐시 |
| `ChainMap` | 여러 딕셔너리를 하나처럼 조회 | 설정값 관리 |
| `namedtuple` | 이름으로 접근하는 튜플 생성 | 좌표, 레코드 |
| `UserDict` | 딕셔너리 동작을 사용자 정의 | 커스텀 딕셔너리 |
| `UserList` | 리스트 동작을 사용자 정의 | 커스텀 리스트 |
| `UserString` | 문자열 동작을 사용자 정의 | 커스텀 문자열 |


## 파일 역할

| 파일 | 역할 |
|---|---|
| `main.py` | 실행 진입점 |
| `models.py` | Commit 데이터 모델 |
| `cli.py` | 명령어 파싱, 입력 검증, REPL, 출력 |
| `repository.py` | 저장소·브랜치·커밋·역색인 관리 |
| `algorithms.py` | 위상 정렬, 병합 정렬, DFS, BFS |

## 명령어

| 명령어 | 기능 |
|---|---|
| `INIT <user_name>` | 저장소 초기화 및 사용자 설정 |
| `BRANCH <branch_name>` | 현재 HEAD 기준 브랜치 생성 |
| `SWITCH <branch_name>` | 브랜치 전환 |
| `COMMIT <message>` | 커밋 생성 및 역색인 갱신 |
| `LOG` | 부모 우선 로그 출력 |
| `LOG --sort-by=date` | 날짜 오름차순 |
| `LOG --sort-by=author` | 작성자 오름차순 |
| `PATH <commit1> <commit2>` | 무방향 최단 경로 |
| `ANCESTORS <commit_hash>` | 모든 조상 탐색 |
| `SEARCH <keyword>` | 메시지 키워드 검색 |
| `SEARCH --author=<name>` | 작성자 검색 |
| `exit` / `quit` | 프로그램 종료 |


## 공통 실행 흐름

```text
main.py → cli.py: repl()
    ↓
cli.py: execute() → 명령어 파싱 및 인자 검증
    ↓
repository.py: Repository 메서드 호출
    ↓
algorithms.py: 알고리즘 실행 (필요 시)
    ↓
repository.py → 결과 반환
    ↓
cli.py: 출력 문자열 변환
    ↓
cli.py: repl() → print(result)
```

### 저장소 관리 명령어

| 입력 | Repository 메서드 | 주요 처리 |
|---|---|---|
| `init "admin"` | `init()` | 상태 초기화, main 및 사용자 설정 |
| `branch dev` | `branch()` | 현재 커밋을 참조하는 브랜치 생성 |
| `switch dev` | `switch()` | HEAD를 dev로 변경 |
| `commit "Add login"` | `commit()` | Commit 생성, hash·브랜치·역색인 갱신 |


### 알고리즘 실행 명령어

| 입력 | Repository 메서드 | algorithms.py 함수 |
|---|---|---|
| `log` | `log()` | `parent_first()` |
| `log --sort-by=date` | `log("date")` | `parent_first()` → `merge_sort()` |
| `log --sort-by=author` | `log("author")` | `parent_first()` → `merge_sort()` |
| `path 000001 000003` | `path()` | `shortest_path()` |
| `ancestors 000003` | `ancestor_hashes()` | `ancestors()` |


### 검색 및 종료

| 입력 | 처리 |
|---|---|
| `search login` | `search_keyword()` → keyword_index 조회 |
| `search --author=admin` | `search_author()` → author_index 조회 |
| `quit` / `exit` | `execute()`가 None 반환 → REPL 종료 |

잘못된 인자는 `MiniGitError("Invalid args")`로 처리하며, 오류 발생 후에도 REPL은 유지됩니다.


## 핵심 알고리즘

| 알고리즘 | 함수 | 핵심 자료구조 | 시간복잡도 |
|---|---|---|---|
| Kahn 위상 정렬 | `parent_first()` | dict, deque | O(V + E) |
| 병합 정렬 | `merge_sort()` | list, 재귀 | O(n log n) |
| DFS | `ancestors()` | Stack, set | O(V + E) |
| BFS | `shortest_path()` | Queue, dict, set | O(V + E) |

- **위상 정렬:** 부모 커밋이 자식보다 먼저 출력되도록 처리합니다.
- **병합 정렬:** 날짜·작성자 기준 오름차순 안정 정렬을 수행합니다.
- **DFS:** Stack으로 모든 조상 커밋을 중복 없이 탐색합니다.
- **BFS:** 무방향 연결의 최단 거리를 계산하고, 최단 경로가 여러 개면 사전순으로 가장 작은 경로를 선택합니다.

커밋은 hash 기반 `dict`에 저장하며, 키워드·작성자 역색인은 `dict[str, set[str]]`로 관리합니다.



## 저장소 및 커밋 데이터 생성
```text
init "admin"
commit "Initial commit"
branch dev
switch dev
commit "Add login"
commit "Update login"
switch main
commit "Add payment"
```


## 알고리즘 4가지 실행 테스트
```text
log
log --sort-by=date
log --sort-by=author
ancestors 000003
path 000003 000004
quit
```


## CLI 정상·예외·경계 조건 테스트

```bash
python main.py
```

```text
init "admin"
branch dev
switch dev
log
commit "A"
ancestors 000001
search a
commit "unfinished
init Bob
log
path 000001 000001
quit
```

검증 항목:
- **정상:** 초기화, 브랜치 생성·전환, 커밋, 검색, 종료
- **예외:** 닫히지 않은 따옴표, 존재하지 않는 커밋
- **경계:** 빈 로그, 한 글자 메시지, 최초 커밋의 조상, 재초기화

### 별도 예외 조건 테스트

프로그램을 새로 실행한 후 입력합니다.

```text
log
branch feature
init "admin"
commit "Initial commit"
branch feature
branch feature
switch unknown
log --sort-by=bad
commit
quit
```

### 잘못된 명령어 및 인자 검증

| 사용자 입력 | 오류 원인 | 출력 결과 |
|---|---|---|
| `init` | 사용자명 누락 | `Invalid args` |
| `branch` | 브랜치 이름 누락 | `Invalid args` |
| `switch dev test` | 인자 개수 초과 | `Invalid args` |
| `commit "   "` | 공백만 있는 메시지 | `Invalid args` |
| `log --sort-by=bad` | 지원하지 않는 옵션 | `Invalid args` |
| `path 000001` | hash 인자 누락 | `Invalid args` |
| `search --author=` | 작성자 누락 | `Invalid args` |
| `quit now` | 불필요한 인자 | `Invalid args` |
