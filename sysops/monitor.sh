#!/bin/bash

# 명령 출력 형식을 영문으로 고정
export LC_ALL=C

# 애플리케이션과 로그 기본 설정
APP_NAME="agent-app-linux-x86"
APP_PORT="15034"
LOG_FILE="/var/log/agent-app/monitor.log"
MAX_SIZE=$((10 * 1024 * 1024))
MAX_FILES=10

# 시스템 자원 경고 임계값 설정
CPU_LIMIT=20
MEM_LIMIT=10
DISK_LIMIT=80

echo "====== SYSTEM MONITOR RESULT ======"
echo "[HEALTH CHECK]"

# 로그 디렉터리와 로그 파일의 존재 및 쓰기 권한 확인
LOG_DIR=$(dirname "$LOG_FILE")

if [ ! -d "$LOG_DIR" ]; then
    echo "[ERROR] Log directory not found: $LOG_DIR"
    exit 1
fi

if [ ! -w "$LOG_DIR" ]; then
    echo "[ERROR] Log directory is not writable: $LOG_DIR"
    exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
    if ! touch "$LOG_FILE"; then
        echo "[ERROR] Failed to create log file: $LOG_FILE"
        exit 1
    fi

    if ! chgrp agent-core "$LOG_FILE"; then
        echo "[ERROR] Failed to set log group: agent-core"
        exit 1
    fi

    if ! chmod 660 "$LOG_FILE"; then
        echo "[ERROR] Failed to set log permission: $LOG_FILE"
        exit 1
    fi
fi

if [ ! -w "$LOG_FILE" ]; then
    echo "[ERROR] Log file is not writable: $LOG_FILE"
    exit 1
fi

# 가장 오래된 애플리케이션 프로세스 PID를 대표 PID로 선택
PID=$(pgrep -fo "$APP_NAME")

if [ -z "$PID" ]; then
    echo "Checking process '$APP_NAME'... [FAIL]"
    exit 1
fi

echo "Checking process '$APP_NAME'... [OK] (PID: $PID)"

# TCP 15034 포트의 LISTEN 상태 확인
if ss -ltnH | awk -v port="$APP_PORT" '
    $4 ~ (":" port "$") {found = 1}
    END {exit !found}
'; then
    echo "Checking port $APP_PORT... [OK]"
else
    echo "Checking port $APP_PORT... [FAIL]"
    exit 1
fi

# UFW 또는 firewalld의 활성 상태 확인
echo "[FIREWALL CHECK]"

if command -v ufw >/dev/null 2>&1; then
    if grep -q '^ENABLED=yes' /etc/ufw/ufw.conf 2>/dev/null; then
        echo "UFW status... [OK]"
    else
        echo "[WARNING] UFW is inactive"
    fi
elif command -v firewall-cmd >/dev/null 2>&1; then
    if firewall-cmd --state 2>/dev/null | grep -q '^running$'; then
        echo "firewalld status... [OK]"
    else
        echo "[WARNING] firewalld is inactive"
    fi
else
    echo "[WARNING] No supported firewall tool found"
fi

# CPU·메모리·루트 디스크 사용률 수집
CPU_USAGE=$(top -bn1 | awk '
    /^%?Cpu\(s\):/ {
        printf "%.1f", 100 - $8
        exit
    }
')

MEM_USAGE=$(free | awk '
    /^Mem:/ {
        printf "%.1f", ($3 / $2) * 100
    }
')

DISK_USED=$(df -P / | awk '
    NR == 2 {
        gsub("%", "", $5)
        print $5
    }
')

# 시스템 자원 수집 실패 여부 확인
if [ -z "$CPU_USAGE" ]; then
    echo "[ERROR] Failed to collect CPU usage"
    exit 1
fi

if [ -z "$MEM_USAGE" ]; then
    echo "[ERROR] Failed to collect memory usage"
    exit 1
fi

if [ -z "$DISK_USED" ]; then
    echo "[ERROR] Failed to collect disk usage"
    exit 1
fi

echo "CPU Usage : ${CPU_USAGE}%"
echo "MEM Usage : ${MEM_USAGE}%"
echo "DISK Used : ${DISK_USED}%"

# 임계값을 초과하면 경고만 출력하고 계속 실행
if awk -v value="$CPU_USAGE" -v limit="$CPU_LIMIT" \
    'BEGIN { exit !(value > limit) }'; then
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_LIMIT}%)"
fi

if awk -v value="$MEM_USAGE" -v limit="$MEM_LIMIT" \
    'BEGIN { exit !(value > limit) }'; then
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_LIMIT}%)"
fi

if awk -v value="$DISK_USED" -v limit="$DISK_LIMIT" \
    'BEGIN { exit !(value > limit) }'; then
    echo "[WARNING] DISK threshold exceeded (${DISK_USED}% > ${DISK_LIMIT}%)"
fi

# 로그가 10MB 이상이면 회전 로그를 최대 10개까지 유지
LOG_SIZE=$(stat -c%s "$LOG_FILE")

if [ "$LOG_SIZE" -ge "$MAX_SIZE" ]; then
    echo "[INFO] Log rotation started: ${LOG_SIZE} bytes"

    rm -f "${LOG_FILE}.${MAX_FILES}"

    for i in $(seq $((MAX_FILES - 1)) -1 1); do
        if [ -f "${LOG_FILE}.${i}" ]; then
            if ! mv "${LOG_FILE}.${i}" "${LOG_FILE}.$((i + 1))"; then
                echo "[ERROR] Failed to rotate ${LOG_FILE}.${i}"
                exit 1
            fi
        fi
    done

    if ! mv "$LOG_FILE" "${LOG_FILE}.1"; then
        echo "[ERROR] Failed to rotate current log file"
        exit 1
    fi

    if ! touch "$LOG_FILE"; then
        echo "[ERROR] Failed to create new log file"
        exit 1
    fi

    if ! chgrp agent-core "$LOG_FILE"; then
        echo "[ERROR] Failed to set new log group"
        exit 1
    fi

    if ! chmod 660 "$LOG_FILE"; then
        echo "[ERROR] Failed to set new log permission"
        exit 1
    fi

    echo "[INFO] Log rotation completed"
fi

# 현재 시스템 상태를 지정 형식으로 로그에 누적 기록
NOW=$(date "+%Y-%m-%d %H:%M:%S")
LOG_LINE="[$NOW] PID:$PID CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USED}%"

if echo "$LOG_LINE" >> "$LOG_FILE"; then
    echo "[INFO] Log appended: $LOG_FILE"
else
    echo "[ERROR] Failed to append log: $LOG_FILE"
    exit 1
fi

# 모든 점검과 로그 기록이 성공하면 정상 종료
exit 0
