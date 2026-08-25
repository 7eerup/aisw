## SSH(Secure Shell)
- SSH(Secure Shell) = 원격 접속 통신 규칙(프로토콜)
- OpenSSH = SSH 접속 서버 운영 키 인증 파일 전송 등을 제공하는 SSH 도구 모음


## SSH 포트 20022 및 Root 원격 접속 차단

- /etc/ssh/sshd_config = SSH 서버 데몬(sshd) 접속 정책/보안 설정 관리하는 파일
- SSH 기본 포트 22번 -> 20022번 변경
- PermitRootLogin root 계정 SSH 접속 허용 여부 no 설정 Root 계정 직접 원격 로그인 차단
- ss 명령으로 20022번 포트가 LISTEN 상태 검증
- 20022/tcp → SSH 원격 접속
- 15034/tcp → Agent 애플리케이션 통신


### 접속 테스트
```bash
ssh -p 20022 <username>@<server-ip>
ssh -p 22 <username>@<server-ip>
```


## 방화벽 활성화 및 허용 포트 제한 테스트

- `sudo ufw status numbered`
- UFW를 활성화 기본 인바운드 정책을 차단으로 설정
- 외부 접근이 필요한 SSH 포트 20022/tcp와 Agent 애플리케이션 포트 15034/tcp 허용 
- ufw status numbered verbose 실제 적용 상태 기본 정책 검증
- `/tcp` = TCP(Transmission Control Protocol) 네트워크 전송 프로토콜


## 계정·그룹 구성
```bash
getent group agent-common
getent group agent-core

id agent-admin
id agent-dev
id agent-test
```
```
agent-common = 공용 그룹 역할
 ├─ agent-admin = 애플리케이션 실행·운영
 ├─ agent-dev = monitor.sh 개발·관리
 └─ agent-test = 테스트 수행·민감 파일 접근 불가

agent-core = 핵심 운영/개발 역할
 ├─ agent-admin = monitor.sh 운영 및 로그 관리
 └─ agent-dev = 개발 및 핵심 파일 관리
```



## Boot Sequence 5단계 [OK] 및 "Agent READY" 출력

### 기존 실행 프로세스 확인
```bash
pgrep -af agent-app-linux-x86
sudo ss -tulnp | grep 15034
```

```bash
pkill -f agent-app-linux-x86
kill <PID>
```

### agent-admin으로 애플리케이션 실행
```bash
sudo -iu agent-admin
source ~/.bashrc
cd "$AGENT_HOME"
./agent-app-linux-x86
```

### 포트 확인
```bash
sudo ss -tulnp | grep 15034
```

## monitor.sh가 프로세스/포트 상태 점검 비정상 상태에서 exit 1 종료

### monitor.sh Health Check
```bash
sudo -u agent-admin \
/home/agent-admin/agent-app/bin/monitor.sh

echo "exit status=$?"
```


### 비정상 상태 테스트
목적 = 의도적 앱 실행 종료 프로세스/포트 상황 발생 -> 스크립트 [FAIL] exit1 종료
```bash
sudo ss -tulnp | grep 15034
```

```bash
sudo -u agent-admin \
/home/agent-admin/agent-app/bin/monitor.sh

echo "exit status=$?"
```

### 학습 포인트
- 비정상 상태 테스트의 목적 = monitor.sh 장애를 올바르게 감지하는지 검증
- 정상 상태: 앱 실행 중이면 프로세스/포트 정상 판단하고 exit 0
- 비정상 상태: 앱 종료되면 프로세스/포트 이상 감지하고 exit 1
- 실제 운영 환경에서는 애플리케이션이 예기치 않게 종료될 수 있기 때문에 이때 관제 스크립트가 이를 즉시 감지해야 관리자나 자동 복구 시스템 대응



## /var/log/agent-app/monitor.log가 지정 포맷으로 누적 기록

```bash
sudo tail -n 5 /var/log/agent-app/monitor.log
```

```
>>는 기존 내용을 유지하면서 로그를 누적(Append) 한다.
운영 환경에서는 과거 기록을 유지해야 장애 분석이 가능하다.
로그 포맷을 고정하면 사람이 읽기 쉽고, grep, awk 등의 도구로 자동 분석하기도 편리하다.
```


## cron 매분 자동 증가 테스트
```bash
sudo crontab -u agent-admin -e
sudo crontab -u agent-admin -l
systemctl is-active cron
```

### 테스트 전
```bash
sudo wc -l /var/log/agent-app/monitor.log
sudo tail -3 /var/log/agent-app/monitor.log
```

### 60 초 후 줄 수와 최신 시간이 증가하면 정상
```bash
sudo wc -l /var/log/agent-app/monitor.log
sudo tail -3 /var/log/agent-app/monitor.log
```


monitor.sh 수동 실행/자동 실행 모두 지원
수동 실행 = 즉시 상태를 점검하기 위한 용도
자동 실행 = 지속적으로 상태를 점검하고 monitor.log에 누적 기록
cron = Linux에서 명령이나 스크립트를 예약된 시간마다 자동 실행 프로그램
monitor.sh 매분 실행하여 monitor.log를 자동으로 누적 기록하는 역할
tail 확인 monitor.log 1분 간격 기록

crontab = cron이 읽는 예약 작업 설정 파일
crontab 시간 필드 = ***** 매월 매일 매시간 매분 요일 관계없이 monitor.sh 실행



## monitor.log 용량 관리(10MB/10개) 설정/동작 설명

### 설정 확인

```bash
sudo grep -nE 'MAX_SIZE|MAX_FILES|LOG_SIZE|stat -c%s|seq|mv|touch|chmod|chown' /home/agent-admin/agent-app/bin/monitor.sh


10:MAX_SIZE=$((10 * 1024 * 1024))
11:MAX_FILES=10
35:    if ! touch "$LOG_FILE"; then
45:    if ! chmod 660 "$LOG_FILE"; then
168:LOG_SIZE=$(stat -c%s "$LOG_FILE")
170:if [ "$LOG_SIZE" -ge "$MAX_SIZE" ]; then
171:    echo "[INFO] Log rotation started: ${LOG_SIZE} bytes"
173:    rm -f "${LOG_FILE}.${MAX_FILES}"
175:    for i in $(seq $((MAX_FILES - 1)) -1 1); do
177:            if ! mv "${LOG_FILE}.${i}" "${LOG_FILE}.$((i + 1))"; then
184:    if ! mv "$LOG_FILE" "${LOG_FILE}.1"; then
189:    if ! touch "$LOG_FILE"; then
199:    if ! chmod 660 "$LOG_FILE"; then
```

```
monitor.log 용량 관리는 현재 로그 파일이 10MB 이상이 되면 회전(rotation)시키고, 과거 로그를 최대 10개까지 유지하는 방식
최대 크기: MAX_SIZE=$((10 * 1024 * 1024))로 monitor.log 회전 기준을 10MB로 설정
최대 보존 수: MAX_FILES=10으로 회전 로그를 monitor.log.1부터 monitor.log.10까지 유지
크기 확인: stat -c%s로 현재 로그 파일 크기를 바이트 단위로 조회
회전 조건: 로그 크기가 10MB 이상이면 회전 시작
파일 이동: 기존 로그를 큰 번호부터 역순으로 이동하고, 현재 로그를 monitor.log.1로 변경
새 로그 생성: touch로 새 monitor.log를 만들고 chmod 660으로 권한 설정
오래된 로그 정리: 가장 오래된 monitor.log.10을 삭제해 회전 파일이 10개를 넘지 않도록 관리

monitor.log       최신 로그 기록 중
monitor.log.1     직전에 회전된 로그
monitor.log.2     그보다 이전 로그
...
monitor.log.10    가장 오래된 보관 로그
```

### 회전 로그 파일 확인
```bash
sudo bash -c 'ls -lh /var/log/agent-app/monitor.log*'
```


## monitor.sh에서 프로세스 식별(pgrep/ps 등)과 포트 확인(ss/netstat 등)에 사용한 명령과 선택 이유

### 프로세스 식별 선택 이유
- pgrep = 실행 프로세스/PID 확인
- -f : 프로세스 이름뿐만 아니라 전체 실행 명령행을 기준으로 검색
- -o : 여러 프로세스가 검색될 경우 가장 오래된 프로세스 하나의 PID를 선택
- 프로세스 이름이나 실행 명령을 검색해서 PID를 바로 얻을 수 있기 때문

- pgrep은 실행 중인 프로세스를 이름으로 검색하고 PID를 바로 확인할 수 있습니다.



### 포트 확인 선택 이유
- ss = TCP 15034 LISTEN 확인
- ss: 소켓 상태 확인 l: LISTEN 상태 t: TCP n: 포트 번호 H: 헤더 제거
- iproute2 = 리눅스 최신 네트워크 관리 도구 모음
- iproute2 ss 기본 제공 현재 소켓과 LISTEN 포트 상태 빠른 확인 적합
- netstat 사용하려면 별도로 net-tools 패키지 설치 의존성 줄임



## CPU/MEM/DISK 값을 어떤 방식으로 추출/파싱 로그 포맷을 왜 그 형태로 고정했는지 설명


### CPU/MEM/DISK 값 추출·파싱 방식
- POSIX(Portable Operating System Interface) 표준 출력
- awk = 텍스트를 검색·추출·계산하는 도구 → 필요한 값 추출·계산
- 고정 로그 포맷 → 추적과 자동 분석을 쉽게 하기 위해
- CPU: `top -bn1` CPU 사용률 1회 수집
- 메모리: `free`로 전체·사용 메모리 조회 및 사용률 계산
- 디스크: `df -P /`로 루트 파일시스템 사용률을 확인하고, `-P` 옵션으로 POSIX 형식 출력 후 `awk`로 안정적으로 파싱


### CPU/Memory/Process 실시간 확인
```bash
top
top -bn1
```

### 메모리/Swap 사용량 확인
```bash
free
free -h -m -g
```

### Disk/FileSystem 사용량 확인
```bash
df
df -h
df -P /
df -T /
```
- tmpfs = RAM을 사용하는 임시 파일시스템(용도별 여러 개 생성)
- /dev/shm = 공유 메모리
- /run 시스템 실행 정보 
- /run/lock = 잠금 파일 
- /run/user/UID = 사용자별 런타임 데이터 저장


### 파싱(Parsing)
파싱은 명령어가 출력한 결과에서 필요한 값만 뽑아 변수에 저장하는 과정입니다. 이번에는 awk를 이용해 CPU, 메모리, 디스크 사용률만 추출했습니다.


### buff/cache
- 버퍼와 캐시는 디스크 접근 속도를 높이기 위해 리눅스가 임시로 사용하는 메모리
- cat hello.txt
- 재실행 리눅스는 파일 내용을 메모리에 저장해 두었다가 더 빠르게 제공(페이지 캐시 메모리)
- 자주 읽는 설정 파일
- 실행 프로그램의 코드
- 웹 서버가 제공한 이미지 파일
- 데이터베이스에서 읽은 파일 데이터


### 로그 포맷을 고정한 이유

- 시간순 장애 추적이 쉬움
- 어떤 프로세스를 점검했는지 PID로 확인 가능
- CPU·메모리·디스크 값을 한 줄에서 비교 가능
- grep, awk, cut 같은 명령으로 자동 분석하기 쉬움
- cron이 반복 기록해도 각 줄의 구조가 동일함
- 향후 로그 수집·시각화 도구와 연동하기 쉬움



## 소유자(agent-dev) 실행자(agent-admin, cron) 권한 정책을 어떻게 만족시켰는지(소유/그룹/권한) 설명

- 소유자: monitor.sh의 소유자를 agent-dev로 설정하여 스크립트 수정 권한을 부여
- 그룹: agent-core로 설정하여 agent-admin이 그룹 권한으로 실행 가능하도록 구성
- 권한: 750(rwxr-x---)으로 소유자는 읽기·쓰기·실행, 그룹은 읽기·실행, 그 외 사용자는 접근 차단
- cron: agent-admin 계정의 crontab에 등록하여 매분 monitor.sh를 자동 실행



## 용량 기반 로그 관리(10MB/10개)를 monitor.sh 내부 코드로 직접 구현 설명

- 구현 방식: monitor.sh 내부 코드로 직접 구현
- 크기 확인: `stat -c%s /var/log/agent-app/monitor.log` 크기를 바이트 단위로 조회
- 회전 조건: 로그 크기가 10MB 이상이면 현재 로그를 monitor.log.1로 이동
- 보존 정책: 기존 로그를 .1 → .2 … .9 → .10으로 이동하고 가장 오래된 .10은 삭제
- 새 로그 생성: 빈 monitor.log를 다시 만들고 권한 660, 그룹 agent-core 적용
- 결과: 최신 로그 1개와 회전 로그 최대 10개를 유지해 디스크 사용량 증가를 제한




## SSH 포트 변경과 Root 접속 차단이 왜 보안에 효과적인지 위협 모델 관점에서 설명

- SSH 포트 변경: 자동 스캔·무차별 대입 공격 노출 감소 (100% 방어 불가능)
- Root 접속 차단: 최고 권한 계정의 직접 로그인 차단으로 권한 탈취 위험 감소
- 목적: 공격 표면을 줄이고, 일반 계정 + sudo 방식으로 시스템 보안 강화



## api_keys와 로그 디렉토리를 agent-core로 제한한 이유를 “최소 권한 원칙”으로 설명
- 최소 권한 원칙: 필요한 사용자에게만 필요한 권한만 부여
- api_keys: API 키 등 민감 정보를 보호하기 위해 agent-core만 접근 허용
- 로그 디렉터리: 운영·개발 계정만 로그를 조회·기록하도록 agent-core로 제한
- 목적: 불필요한 접근을 차단하여 정보 유출과 오작동 위험을 줄임


## “경고는 출력하되 종료하지 않는 항목”(방화벽 비활성/임계치 초과)을 분리한 운영상의 이유
즉시 장애 항목: 프로세스·포트 이상은 서비스 제공이 불가능하므로 exit 1로 종료
경고 항목: 방화벽 비활성이나 CPU·MEM·DISK 임계치 초과는 위험 신호지만 서비스가 계속 동작할 수 있어 경고만 출력
운영 목적: 불필요한 장애 판정을 줄이고, 서비스 지속성과 이상 징후 관찰을 동시에 유지
대응 방식: 경고가 반복되면 운영자가 설정 점검, 자원 증설, 원인 분석을 수행

방화벽 비활성이나 자원 임계치 초과는 즉시 서비스 장애를 의미하지 않기 때문에 스크립트를 종료하지 않고 경고만 남겼습니다. 반면 프로세스나 포트 이상은 실제 서비스 중단 상태이므로 exit 1로 구분했습니다.


## 리다이렉션 기호 > 와 >> 차이점 로그 누적에 >> 필요한 이유

- `> 출력 리다이렉션(덮어쓰기)` : 기존 내용을 지우고 새 내용으로 덮어씀
- `>> 출력 리다이렉션(추가, Append)` : 기존 내용을 유지하고 끝에 이어서 기록
- 로그는 이전 기록을 보존해야 하므로 `>>`를 사용해 누적 저장

- 매분 생성되는 로그를 이전 기록과 함께 계속 저장
- 장애 발생 시 과거 이력을 확인 가능
- 로그 회전(10MB/10개) 전까지 모든 기록을 누적 관리 가능

```bash
echo "test1" > log.txt
echo "test2" > log.txt
```


## 모니터링 대상을 Nginx로 변경할 때 monitor.sh 내부 변수 설정

- 프로세스: APP_NAME="nginx"로 변경하고 pgrep 또는 systemctl is-active nginx로 실행 상태 확인
- 포트: APP_PORT="80" 또는 HTTPS 사용 시 443으로 변경하고 ss로 LISTEN 상태 확인
로그: /var/log/nginx/access.log, /var/log/nginx/error.log의 존재 여부와 오류 발생 여부를 점검
- 임계값: 실제 웹 트래픽과 서버 사양에 맞게 CPU·MEM·DISK 기준을 재설정


### Nginx 설치/서비스/프로세스/포트
```bash
sudo apt update
sudo apt install -y nginx

sudo systemctl enable nginx
sudo systemctl start nginx
systemctl status nginx

pgrep -af nginx
sudo ss -ltnp | grep ':80'
sudo ss -ltnp | grep ':443'
sudo ls -l /var/log/nginx/
sudo tail -10 /var/log/nginx/access.log
curl http://localhost
```

### monitor.sh 내부 변수 설정
```bash
APP_NAME="nginx"
APP_PORT="80"
ACCESS_LOG="/var/log/nginx/access.log"
ERROR_LOG="/var/log/nginx/error.log"
```






## “프로세스는 살아있는데 포트가 안 열리는 상황”을 발견했다면, 원인 문제 해결 방법

```bash
# 1. 프로세스 확인
pgrep -af nginx

# 2. 포트 확인
sudo ss -ltnp | grep :80

# 3. 로그 확인
sudo tail -20 /var/log/nginx/error.log

# 4. 설정 확인
sudo nginx -t

# 5. 포트 충돌 확인
sudo ss -ltnp | grep :80
```

- 1순위: 프로세스 실행 확인 (pgrep, ps, systemctl)
- 2순위: 포트 LISTEN 확인 (ss)
- 3순위: 애플리케이션 로그 확인 (error.log, monitor.log)
- 4순위: 설정 및 환경 확인 (포트 설정, 권한, 방화벽)


### 원인 후보
- 프로세스는 실행 중이지만 포트 바인딩 실패
- 잘못된 포트 번호로 실행
- 설정 파일 오류로 서비스가 정상 시작되지 않음
- 포트가 다른 프로세스에서 이미 사용 중
- 방화벽 또는 보안 정책으로 접속 차단


## 로그가 급증해 디스크가 가득 찰 위험이 있다면, 운영자가 취할 대응(단기/중기) 설명

- 단기 대응: 로그 회전, 오래된 로그 삭제·압축, 불필요한 로그 레벨 감소로 디스크 공간 확보
- 중기 대응: logrotate 적용, 보관 기간 정책 수립, 중앙 로그 서버(ELK 등)로 로그 분리
- 목적: 디스크 부족으로 서비스가 중단되는 것을 예방




## agent-app-linux-x86 AMD64 아키텍처용 실행 파일 역할
```
agent-app-linux-x86
        │
        ▼
실행
        │
        ▼
Boot Sequence 수행
        │
        ├─ 사용자 확인
        ├─ 환경 변수 확인
        ├─ secret.key 확인
        ├─ 포트 확인
        └─ 로그 디렉터리 확인
        │
        ▼
Agent READY
        │
        ▼
15034 포트 서비스 시작(LISTEN)
```

## monitor.sh 감시 역할
```
agent-app-linux-x86 (서비스)
        │
        ▼
15034 포트 오픈
        │
        ▼
monitor.sh
        ├─ 프로세스 확인
        ├─ 포트 확인
        ├─ CPU/MEM/DISK 확인
        └─ monitor.log 기록
```

## monitor.sh 동작

```bash
monitor.log
      │
      ▼
10MB 미만
      │
      ▼
로그 계속 누적 (>>)
      │
      ▼
10MB 초과
      │
      ▼
로그 회전(Rotation)
      │
      ├─ monitor.log → monitor.log.1
      ├─ 새 monitor.log 생성
      └─ 최대 10개 유지
             │
             ▼
11번째 로그가 생기면 가장 오래된 로그 삭제
```

- 로그가 무한정 증가하는 것을 방지
- 디스크 공간 부족 예방
- 최근 로그는 유지하면서 오래된 로그는 자동 정리
- 장기간 운영 시 안정적인 로그 관리 가능