# 수행 내역

## 환경 설정(SSH 포트, 방화벽 규칙, 계정/그룹/ACL, 디렉토리/권한, 환경 변수, cron 등록)


### SSH 포트 변경(20022) 및 Root 원격 접속 차단 설정
```bash
sudo nano /etc/ssh/sshd_config
```

### 문법 검사
```bash
sudo sshd -t
```

### ssh.socket 비활성화
```bash
sudo systemctl stop ssh.socket
sudo systemctl disable ssh.socket
sudo systemctl restart ssh
```

### SSH 설정 확인
```bash
grep -nE '^Port|^PermitRootLogin' /etc/ssh/sshd_config
sudo sshd -T | grep -E '^port|^permitrootlogin'
sudo ss -tulnp | grep 20022
```


### 방화벽 설정


#### UFW 활성화
```bash
sudo ufw enable
```

#### 기존 22번 규칙 삭제
```bash
sudo ufw delete allow 22/tcp
```

#### 포트 허용
```bash
sudo ufw allow 20022/tcp
sudo ufw allow 15034/tcp
```

#### 설정 확인
```bash
sudo ufw status numbered
sudo ufw status verbose
```


### 계정 및 그룹 생성
```bash
sudo groupadd agent-common
sudo groupadd agent-core
```

### 사용자 생성
```bash
sudo useradd -m agent-admin
sudo useradd -m agent-dev
sudo useradd -m agent-test
```

### 그룹 추가
```bash
sudo usermod -aG agent-common agent-admin
sudo usermod -aG agent-core agent-admin

sudo usermod -aG agent-common agent-dev
sudo usermod -aG agent-core agent-dev

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


### 디렉터리 및 ACL 권한 설정
```bash
sudo mkdir -p /home/agent-admin/agent-app/{upload_files,api_keys,bin}
sudo mkdir -p /var/log/agent-app
```

### 키 파일 설정

```bash
echo "agent_api_key_test" | sudo tee /home/agent-admin/agent-app/api_keys/secret.key > /dev/null

sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys/secret.key

sudo chmod 660 /home/agent-admin/agent-app/api_keys/secret.key
```

### 소유자 및 그룹 설정
```bash
sudo chown agent-admin:agent-core /home/agent-admin/agent-app
sudo chown agent-admin:agent-common /home/agent-admin/agent-app/upload_files
sudo chown agent-admin:agent-core /home/agent-admin/agent-app/api_keys
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin
sudo chown root:agent-core /var/log/agent-app
```

### 권한 설정
```bash
sudo chmod 750 /home/agent-admin/agent-app
sudo chmod 770 /home/agent-admin/agent-app/upload_files
sudo chmod 770 /home/agent-admin/agent-app/api_keys
sudo chmod 770 /home/agent-admin/agent-app/bin
sudo chmod 770 /var/log/agent-app
```

### 애플리케이션 실행 파일 설정

```bash
uname -m
```

```bash
sudo cp agent-app-linux-x86 /home/agent-admin/agent-app/

sudo chown agent-admin:agent-core /home/agent-admin/agent-app/agent-app-linux-x86

sudo chmod 750 /home/agent-admin/agent-app/agent-app-linux-x86

sudo ls -l /home/agent-admin/agent-app/agent-app-linux-x86
```

### ACL 설정
```bash
sudo setfacl -m u:agent-dev:rx /home/agent-admin
sudo setfacl -m u:agent-test:--x /home/agent-admin
sudo setfacl -m u:agent-test:--x /home/agent-admin/agent-app
```

### 확인
```bash
sudo ls -ld \
/home/agent-admin \
/home/agent-admin/agent-app \
/home/agent-admin/agent-app/upload_files \
/home/agent-admin/agent-app/api_keys \
/home/agent-admin/agent-app/bin \
/var/log/agent-app

sudo getfacl /home/agent-admin
sudo getfacl /home/agent-admin/agent-app
sudo getfacl /home/agent-admin/agent-app/upload_files
sudo getfacl /home/agent-admin/agent-app/api_keys
sudo getfacl /var/log/agent-app
```

### 환경 변수 설정
```bash
sudo -u agent-admin nano /home/agent-admin/.bashrc
```

```
export AGENT_HOME=/home/agent-admin/agent-app
export AGENT_PORT=15034
export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files
export AGENT_KEY_PATH=$AGENT_HOME/api_keys
export AGENT_LOG_DIR=/var/log/agent-app
```

### 적용 및 확인
```bash
sudo -u agent-admin bash -ic '
echo AGENT_HOME=$AGENT_HOME
echo AGENT_PORT=$AGENT_PORT
echo AGENT_UPLOAD_DIR=$AGENT_UPLOAD_DIR
echo AGENT_KEY_PATH=$AGENT_KEY_PATH
echo AGENT_LOG_DIR=$AGENT_LOG_DIR
'
```



### monitor.sh 권한 설정
```bash
sudo chown agent-dev:agent-core /home/agent-admin/agent-app/bin/monitor.sh
sudo chmod 750 /home/agent-admin/agent-app/bin/monitor.sh
```

### 확인
```bash
sudo stat -c 'owner=%U group=%G mode=%a path=%n' \
/home/agent-admin/agent-app/bin/monitor.sh
```


### cron 등록 및 확인
```bash
sudo crontab -u agent-admin -e
sudo crontab -u agent-admin -l
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


## 디렉터리 및 ACL 확인

```
drwxr-x---+ 1 agent-admin agent-admin  138 Jun 21 17:22 /home/agent-admin
drwxr-x---+ 1 agent-admin agent-core    84 Jun 20 22:59 /home/agent-admin/agent-app
drwxrwx---  1 agent-admin agent-core    20 Jun 21 16:55 /home/agent-admin/agent-app/api_keys
drwxrwx---  1 agent-dev   agent-core    20 Jun 21 17:41 /home/agent-admin/agent-app/bin
drwxrwx---  1 agent-admin agent-common   0 Aug  2 18:37 /home/agent-admin/agent-app/upload_files
drwxrwx---  1 root        agent-core    48 Jun 21 17:22 /var/log/agent-app


getfacl: Removing leading '/' from absolute path names
# file: home/agent-admin
# owner: agent-admin
# group: agent-admin
user::rwx
user:agent-dev:r-x
user:agent-test:--x
group::r-x
mask::r-x
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