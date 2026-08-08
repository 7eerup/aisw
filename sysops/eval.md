| 항목        | 핵심 확인 내용                                                               |
| ------------ | ---------------------------------------------------------------------- |
| SSH          | `20022` 포트 사용, Root 원격 로그인 차단                                          |
| 방화벽          | UFW 또는 firewalld 활성화, `20022/tcp`, `15034/tcp`만 허용                     |
| 사용자/그룹       | `agent-admin`, `agent-dev`, `agent-test`, `agent-common`, `agent-core` |
| 앱 실행         | Boot Sequence 5단계 `[OK]` + `Agent READY`                               |
| Health Check | 프로세스/15034 포트 정상 확인                                                    |
| 장애 처리        | 프로세스 또는 포트 비정상 → `exit 1`                                              |
| 로그           | `/var/log/agent-app/monitor.log` 누적                                    |
| cron         | `agent-admin` crontab에서 매분 실행                                          |
| 로그 용량        | 최대 `10MB`, 최대 `10개` 관리                                                 |
