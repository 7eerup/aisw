## Docker Compose 멀티 컨테이너 실습 가이드
docker-compose.yml 작성 및 실행
docker-compose ps로 컨테이너 상태 확인
docker network inspect로 네트워크 구조 파악
컨테이너 내부에서 ping/curl로 통신 테스트
서비스명으로 자동 DNS 해석 확인
로그 확인으로 통신 흐름 파악

### 이미지 빌드 + 컨테이너 시작
```bash
$ docker compose up -d --build
```

### 목록 확인
```bash
$ docker-compose ps

NAME          IMAGE                          COMMAND                  SERVICE   CREATED         STATUS         PORTS
fastapi-app   docker-compose-multi-fastapi   "uvicorn app:app --h…"   fastapi   5 minutes ago   Up 5 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
redis-cache   redis:7-alpine                 "docker-entrypoint.s…"   redis     5 minutes ago   Up 5 minutes   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp
```

### 네트워크 통신 확인 및 헬스 체크
```bash
$ curl http://localhost:8000/health

{"fastapi":"✅ OK","redis":"✅ OK","message":"모든 서비스 정상"}
```

### 캐시 기능 테스트 + 데이터 저장
```bash
$ curl -X POST "http://localhost:8000/cache/user:1" \
  -H "Content-Type: application/json" \
  -d '"John Doe"'
```

### 데이터 조회
```bash
$ curl http://localhost:8000/cache/user:1

{"status":"✅ 조회 성공","key":"user:1","value":"John Doe"}
```

### 추가 데이터 저장
```bash
$ curl -X POST "http://localhost:8000/cache/user:2" \
  -H "Content-Type: application/json" \
  -d '"Jane Smith"'
```

### 추가 데이터 조회
```bash
$ curl http://localhost:8000/cache/user:2

{"status":"✅ 조회 성공","key":"user:2","value":"Jane Smith"}
```

### 통계 확인
```bash
$ curl http://localhost:8000/stats
```

### 데이터 삭제
```bash
$ curl -X DELETE http://localhost:8000/cache/user:1

{"status":"✅ 삭제 완료","key":"user:1"}
```

### 컨테이너 내부 접속
```bash
$ docker-compose exec fastapi bash
$ docker-compose exec redis redis-cli
```

### 내부에서 Redis 연결 테스트
```bash
$ python3 -c "
from redis import Redis
r = Redis.from_url('redis://redis:6379', decode_responses=True)
print('✅ Redis 연결 성공!' if r.ping() else '❌ 실패')
"

Redis 연결 성공!
```

### 네트워크 확인
```bash
$ docker network ls | grep compose

d70dad7e63c0   docker-compose-multi_app-network   bridge    local
```

### 네트워크 상세 정보
```bash
$ docker network inspect docker-compose-multi_app-network
```

```
[
    {
        "Name": "docker-compose-multi_app-network",
        "Id": "d70dad7e63c086401af14f8da1154d0322b411afc45f222368f6fc533ca71351",
        "Created": "2026-04-02T21:26:41.81159999+09:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv4": true,
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Options": {},
        "Labels": {
            "com.docker.compose.config-hash": "11ca04733a22c8c0280de3e298c418c705c690dca4287ffa0faf0ba2ac91d7d3",
            "com.docker.compose.network": "app-network",
            "com.docker.compose.project": "docker-compose-multi",
            "com.docker.compose.version": "5.1.1"
        },
        "Containers": {
            "4eeedc9e6866df5690cf36d4828658ea09a1ff4f43a32c693c3b4ff65a6b2c4e": {
                "Name": "redis-cache",
                "EndpointID": "34f8ae8ec06df3932dfe197e9f32f0a228040a78e6dbf5ca627481f1af93a452",
                "MacAddress": "62:d2:57:0c:93:1a",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            },
            "7efa8f2d499c1471b1495d7686b5cff91902c41ab69c3bbd0ddcb3eface4d15b": {
                "Name": "fastapi-app",
                "EndpointID": "507190347ca1c9593afc2090bfcfbb713b51059d71ef532867a404ba37bca1c1",
                "MacAddress": "f2:3c:b0:6d:6e:e7",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
        },
        "Status": {
            "IPAM": {
                "Subnets": {
                    "172.18.0.0/16": {
                        "IPsInUse": 5,
                        "DynamicIPsAvailable": 65531
                    }
                }
            }
        }
    }
]
```

### 전체 로그 확인
```bash
$ docker compose logs
```

### FastAPI만 로그
```bash
$ docker-compose logs fastapi
```

### Redis만 로그
```bash
$ docker-compose logs redis
```

### 실시간 로그
```bash
$ docker-compose logs -f
```


### 종료
```bash
$ docker compose down
```