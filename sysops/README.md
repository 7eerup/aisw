# 수행 내역

## 환경 설정(SSH 포트, 방화벽 규칙, 계정/그룹/ACL, 디렉토리/권한, 환경 변수, cron 등록)

## 기본 보안 및 네트워크 설정


### OpenSSH Server 환경 설정
- openssh-server 설치 → /etc/ssh/sshd_config 생성
- SSH 서버 설정 = /etc/ssh/sshd_config
- Port             → SSH 서비스 포트 설정
- PermitRootLogin  → Root 원격 로그인 허용 여부
- ListenStream     → systemd ssh.socket의 실제 LISTEN 주소·포트

- OrbStack Ubuntu
   - sudo passwd whoami
   - SSH 로그인용 비밀번호 설정

- macOS
   - ssh -p 20022 ...
   - Ubuntu 실제 원격 접속 테스트

- root 시스템 최고 관리자 계정
- 외부에서 root로 직접 SSH 접속하는 경로를 차단하는 보안 설정


### OpenSSH Server 설치
```bash
sudo apt install openssh-server -y
dpkg -l | grep openssh-server
sudo systemctl status ssh
```

### SSH 테스트
```bash
ssh -p 20022 사용자명@IP
ssh -p 22 사용자명@IP
```

### SSH 포트 변경 및 Root 원격 접속 차단 설정
```bash
sudo nano /etc/ssh/sshd_config
```

### 문법 검사 및 SSH 서비스 재시작
```bash
sudo sshd -t
sudo systemctl restart ssh
```

### SSH Socket 상태 및 설정 확인
```bash
systemctl status ssh.socket
systemctl cat ssh.socket
```

### SSH Socket 포트 Override 설정
```bash
sudo systemctl edit ssh.socket
```

### SSH Socket /usr/lib/systemd/system/ssh.socket
.
.
.
[Socket]
ListenStream=
ListenStream=0.0.0.0:20022
ListenStream=[::]:20022


### systemd 설정 반영 및 SSH Socket 재시작
```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```


### SSH 설정 확인
```bash
grep -nE '^Port|^PermitRootLogin' /etc/ssh/sshd_config
sudo sshd -T | grep -E '^port|^permitrootlogin'
sudo ss -tulnp | grep 20022
```



### UFW 방화벽 설정
```bash
which ufw
sudo apt update
sudo apt install ufw -y
```

### 기존 22번 규칙 삭제
```bash
sudo ufw delete allow 22/tcp
```

### 기본 정책 설정
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### SSH 애플리케이션 포트 허용
```bash
sudo ufw allow 20022/tcp
sudo ufw allow 15034/tcp
```

### 등록된 UFW 규칙 확인
```bash
sudo ufw show added
```

#### UFW 활성화
```bash
sudo ufw enable
```

#### UFW 상태 및 허용 규칙 확인
```bash
sudo ufw status numbered
sudo ufw status verbose
```


## 계정/그룹/권한 체계
- 로그 디렉토리 = /var/log/agent-app
- 로그 파일 = /var/log/agent-app/monitor.log
- -m 홈 디렉터리 생성
- -s /bin/bash 로그인 셸 명시적으로 지정

- `chown` → 소유자와 그룹 지정
- `chmod` → 읽기·쓰기·실행 권한 지정


### 계정 그룹 생성 및 확인
```bash
sudo groupadd agent-common
sudo groupadd agent-core

getent group agent-common
getent group agent-core
```

### 사용자 생성 및 확인
```bash
sudo useradd -m -s /bin/bash agent-admin
sudo useradd -m -s /bin/bash agent-dev
sudo useradd -m -s /bin/bash agent-test

getent passwd agent-admin
getent passwd agent-dev
getent passwd agent-test
```

### 그룹 추가
```bash
sudo usermod -aG agent-common,agent-core agent-admin
sudo usermod -aG agent-common,agent-core agent-dev
sudo usermod -aG agent-common agent-test
```

### 확인
```bash
id agent-admin
id agent-dev
id agent-test

getent group agent-common
getent group agent-core
```

### 디렉터리 생성
```bash
sudo mkdir -p /home/agent-admin/agent-app/{upload_files,api_keys,bin}
sudo mkdir -p /var/log/agent-app
```

### 디렉터리 소유자 및 그룹 설정
```bash
sudo chown agent-admin:agent-core /home/agent-admin/agent-app
sudo chown agent-admin:agent-common /home/agent-admin/agent-app/upload_files
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin
sudo chown root:agent-core /var/log/agent-app
```

### 디렉터리 접근 권한 설정
```bash
sudo chmod 750 /home/agent-admin/agent-app
sudo chmod 770 /home/agent-admin/agent-app/upload_files
sudo chmod 770 /home/agent-admin/agent-app/api_keys
sudo chmod 770 /home/agent-admin/agent-app/bin
sudo chmod 770 /var/log/agent-app
```


### 디렉터리 소유자·그룹·권한 확인
```bash
sudo ls -ld /home/agent-admin/agent-app
sudo ls -ld /home/agent-admin/agent-app/upload_files
sudo ls -ld /home/agent-admin/agent-app/api_keys
sudo ls -ld /home/agent-admin/agent-app/bin
sudo ls -ld /var/log/agent-app

getfacl /home/agent-admin/agent-app
getfacl /home/agent-admin/agent-app/upload_files
getfacl /home/agent-admin/agent-app/api_keys
getfacl /home/agent-admin/agent-app/bin
getfacl /var/log/agent-app
```


## 애플리케이션 실행 환경 구성


### 애플리케이션 실행 파일 배치 및 권한 설정

```bash
sudo mkdir -p /home/agent-admin/agent-app
sudo cp agent-app-linux-x86 /home/agent-admin/agent-app/
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/agent-app-linux-x86
sudo chmod 750 /home/agent-admin/agent-app/agent-app-linux-x86
sudo ls -lh /home/agent-admin/agent-app
```


### 환경 변수 등록
```bash
sudo -u agent-admin bash -c 'cat >> /home/agent-admin/.bashrc <<EOF
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=\$AGENT_HOME/upload_files
export AGENT_KEY_PATH=\$AGENT_HOME/api_keys
export AGENT_LOG_DIR=/var/log/agent-app
EOF'
```

### 환경 변수 설정 확인
```bash
sudo tail -n 5 /home/agent-admin/.bashrc
```

### 환경 변수 적용 확인
```
sudo -iu agent-admin

echo $AGENT_HOME
echo $AGENT_PORT
echo $AGENT_UPLOAD_DIR
echo $AGENT_KEY_PATH
echo $AGENT_LOG_DIR
```


### secret.key 설정 및 확인
```bash
sudo touch /home/agent-admin/agent-app/api_keys/secret.key
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys/secret.key
sudo chmod 660 /home/agent-admin/agent-app/api_keys/secret.key

sudo ls -l /home/agent-admin/agent-app/api_keys
```


### 키 파일 설정

```bash
echo "agent_api_key_test" | sudo tee /home/agent-admin/agent-app/api_keys/secret.key > /dev/null
sudo cat /home/agent-admin/agent-app/api_keys/secret.key

sudo ls -l /home/agent-admin/agent-app/api_keys
```

### 로그 디렉터리 소유 그룹 및 권한 설정
```bash
sudo chown root:agent-core /var/log/agent-app
sudo chmod 770 /var/log/agent-app

ls -ld /var/log/agent-app
```

### 로그인 및 환경 변수 적용 확인
```bash
sudo -iu agent-admin

echo $AGENT_HOME
echo $AGENT_PORT
echo $AGENT_UPLOAD_DIR
echo $AGENT_KEY_PATH
echo $AGENT_LOG_DIR
```

### 로그 디렉터리 쓰기 권한 확인
```bash
touch /var/log/agent-app/test.log
ls -l /var/log/agent-app/test.log
rm /var/log/agent-app/test.log
```

### 애플리케이션 실행
```bash
cd /home/agent-admin/agent-app
./agent-app-linux-x86
```

```
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/5] Checking Required Files             [OK]
   ... Verified 'secret.key' with correct key string.
[4/5] Checking Port Availability          [OK]
   ... Port 15034 is available.
[5/5] Verifying Log Permission            [OK]
   ... Log directory is writable: /var/log/agent-app
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
```

### 애플리케이션 15034 포트 LISTEN 확인

```bash
sudo ss -ltnp | grep 15034
```

```
LISTEN 0      1            0.0.0.0:15034      0.0.0.0:*    users:(("agent-app-linux",pid=16149,fd=4))   
```



## 시스템 관제 자동화 스크립트 monitor.sh 구현

### monitor.sh 생성 및 작성
```bash
sudo -u agent-dev nano /home/agent-admin/agent-app/bin/monitor.sh
```

### monitor.sh 소유자·그룹 및 권한 설정
```bash
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh
```

### monitor.sh 소유자·그룹·권한 확인
```bash
sudo ls -l /home/agent-admin/agent-app/bin/monitor.sh
```

### monitor.sh 디렉터리 접근 권한 확인
```bash
sudo -u agent-dev ls -ld /home/agent-admin/agent-app
sudo -u agent-dev ls -ld /home/agent-admin/agent-app/bin
```

### monitor.sh Bash 문법 검사
```bash
sudo -u agent-dev bash -n \
/home/agent-admin/agent-app/bin/monitor.sh
```

### monitor.sh 실행 및 종료 상태 확인(Health Check)
```bash
sudo -u agent-admin /home/agent-admin/agent-app/bin/monitor.sh
echo "exit status=$?"
```

### monitor.log 누적 기록 확인
```bash
sudo ls -l /var/log/agent-app/monitor.log
sudo tail -n 5 /var/log/agent-app/monitor.log
```

### 비정상 상태 exit 1 (애플리케이션 실행 터미널에서 앱 종료 실행)
```bash
sudo -u agent-admin /home/agent-admin/agent-app/bin/monitor.sh
echo "exit status=$?"
```

### 결과
```
echo "exit status=$?"
====== SYSTEM MONITOR RESULT ======
[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [FAIL]
exit status=1
```

### 포트와 자원·방화벽 정상 출력 확인
```bash
sudo -u agent-admin /home/agent-admin/agent-app/bin/monitor.sh
```


### 로그 용량 관리 코드 확인
```bash
sudo grep -nE \
'MAX_SIZE|MAX_FILES|LOG_SIZE|stat -c%s|seq|mv|rm -f' \
/home/agent-admin/agent-app/bin/monitor.sh
```


## cron 매분 자동 실행 등록

### cron 설치 및 서비스 확인
```bash
which cron
sudo apt update
sudo apt install cron -y
sudo systemctl enable --now cron
```


### cron 매분 자동 실행 및 monitor.log 자동 증가 확인
```bash
sudo crontab -u agent-admin -e
```

```
no crontab for agent-admin - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny

Choose 1-3 [1]:
```

* * * * * /home/agent-admin/agent-app/bin/monitor.sh > /dev/null 2>&1

### crontab time field
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 요일
│ │ │ └─── 월
│ │ └───── 일
│ └─────── 시
└───────── 분

→ 매분 실행
```

### crontab 등록 확인
```bash
sudo crontab -u agent-admin -l
```

### monitor.log 자동 증가 확인
```bash
sudo wc -l /var/log/agent-app/monitor.log
sudo tail -n 5 /var/log/agent-app/monitor.log
```









## SSH 포트 변경(20022) 및 Root 원격 접속 차단 설정 확인 내역

```
24:Port 20022
43:PermitRootLogin no

port 20022
permitrootlogin no

tcp   LISTEN 0      128                 0.0.0.0:20022      0.0.0.0:*    users:(("sshd",pid=294,fd=3))            
tcp   LISTEN 0      128                    [::]:20022         [::]:*    users:(("sshd",pid=294,fd=4))
```




## 방화벽(UFW 또는 firewalld) 활성화 및 20022/tcp, 15034/tcp만 허용 내역
```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 20022/tcp                  ALLOW IN    Anywhere                  
[ 2] 15034/tcp                  ALLOW IN    Anywhere                  
[ 3] 20022/tcp (v6)             ALLOW IN    Anywhere (v6)             
[ 4] 15034/tcp (v6)             ALLOW IN    Anywhere (v6)    
```


## 계정/그룹(agent-admin/dev/test, agent-common/core) 생성 확인 내역
```
uid=1000(agent-admin) gid=1002(agent-admin) groups=1002(agent-admin),1000(agent-common),1001(agent-core)
uid=1001(agent-dev) gid=1003(agent-dev) groups=1003(agent-dev),1000(agent-common),1001(agent-core)
uid=1002(agent-test) gid=1004(agent-test) groups=1004(agent-test),1000(agent-common)

agent-common:x:1000:agent-admin,agent-dev,agent-test
agent-core:x:1001:agent-admin,agent-dev
```


## 디렉토리 구조 및 권한(ACL 포함) 확인 내역
```
getfacl: Removing leading '/' from absolute path names
# file: home/agent-admin/agent-app
# owner: agent-admin
# group: agent-core
user::rwx
group::r-x
other::---


getfacl: Removing leading '/' from absolute path names
# file: home/agent-admin/agent-app/upload_files
# owner: agent-admin
# group: agent-common
user::rwx
group::rwx
other::---


getfacl: Removing leading '/' from absolute path names
# file: home/agent-admin/agent-app/api_keys
# owner: agent-admin
# group: agent-core
user::rwx
group::rwx
other::---


getfacl: Removing leading '/' from absolute path names
# file: home/agent-admin/agent-app/bin
# owner: agent-dev
# group: agent-core
user::rwx
group::rwx
other::---



getfacl: Removing leading '/' from absolute path names
# file: var/log/agent-app
# owner: root
# group: agent-core
user::rwx
group::rwx
other::---
```



## Boot Sequence 5단계 [OK] 및 “Agent READY” 확인 내역

```
>>> Starting Agent Boot Sequence...
[1/5] Checking User Account               [OK]
   ... Running as service user 'agent-admin' (uid=1000)
[2/5] Verifying Environment Variables     [OK]
   ... All required Envs correct
[3/5] Checking Required Files             [OK]
   ... Verified 'secret.key' with correct key string.
[4/5] Checking Port Availability          [OK]
   ... Port 15034 is available.
[5/5] Verifying Log Permission            [OK]
   ... Log directory is writable: /var/log/agent-app
------------------------------------------------------------
All Boot Checks Passed!
Agent READY
```



## monitor.sh 실행 결과(프로세스/포트/리소스/경고) 내역

```
====== SYSTEM MONITOR RESULT ======
[HEALTH CHECK]
Checking process 'agent-app-linux-x86'... [OK] (PID: 7001)
Checking port 15034... [OK]
[FIREWALL CHECK]
UFW status... [OK]
CPU Usage : 2.4%
MEM Usage : 30.8%
DISK Used : 16%
[WARNING] MEM threshold exceeded (30.8% > 10%)
[INFO] Log appended: /var/log/agent-app/monitor.log
```


## /var/log/agent-app/monitor.log 누적 기록 확인(최근 라인) 내역

```
[2026-08-02 21:28:02] PID:7001 CPU:3.7% MEM:32.9% DISK_USED:16%
[2026-08-02 21:29:01] PID:7001 CPU:2.5% MEM:30.4% DISK_USED:16%
[2026-08-02 21:30:01] PID:7001 CPU:4.8% MEM:31.1% DISK_USED:16%
[2026-08-02 21:31:02] PID:7001 CPU:2.5% MEM:31.0% DISK_USED:16%
[2026-08-02 21:31:42] PID:7001 CPU:2.4% MEM:30.8% DISK_USED:16%
[2026-08-02 21:32:01] PID:7001 CPU:1.1% MEM:30.6% DISK_USED:16%
[2026-08-02 21:33:01] PID:7001 CPU:4.8% MEM:32.0% DISK_USED:16%
[2026-08-02 21:34:02] PID:7001 CPU:7% MEM:30.2% DISK_USED:16%
[2026-08-02 21:35:01] PID:7001 CPU:100% MEM:31.6% DISK_USED:16%
[2026-08-02 21:36:01] PID:7001 CPU:1.1% MEM:31.7% DISK_USED:16%
```


## crontab 매분 실행 등록 내역

```
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >/dev/null 2>&1
```


## 자동 실행 확인(1분 후 로그 증가) 내역
```
[2026-08-02 21:35:01] PID:7001 CPU:100% MEM:31.6% DISK_USED:16%
[2026-08-02 21:36:01] PID:7001 CPU:1.1% MEM:31.7% DISK_USED:16%
[2026-08-02 21:37:02] PID:7001 CPU:1.1% MEM:32.5% DISK_USED:16%
[2026-08-02 21:38:01] PID:7001 CPU:4.7% MEM:32.5% DISK_USED:16%
[2026-08-02 21:39:01] PID:7001 CPU:4.9% MEM:29.7% DISK_USED:16%
```