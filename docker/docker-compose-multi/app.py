from fastapi import FastAPI, Body
from redis import Redis
import os
import json
from datetime import datetime

app = FastAPI(title="Docker Compose Multi Demo API")

# Redis 연결
redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = Redis.from_url(redis_url, decode_responses=True)

@app.get("/")
def read_root():
    """헬스 체크"""
    return {
        "status": "✅ FastAPI 실행 중",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    """Redis 연결 확인"""
    try:
        redis_client.ping()
        return {
            "fastapi": "✅ OK",
            "redis": "✅ OK",
            "message": "모든 서비스 정상"
        }
    except Exception as e:
        return {
            "fastapi": "✅ OK",
            "redis": "❌ FAIL",
            "error": str(e)
        }

# ✅ 수정: JSON 바디에서 value 받기
@app.post("/cache/{key}")
def set_cache(key: str, value: str = Body(...)):
    """
    Redis에 데이터 저장
    
    예시:
    curl -X POST "http://localhost:8000/cache/user:1" \\
      -H "Content-Type: application/json" \\
      -d '"John Doe"'
    """
    try:
        redis_client.set(key, value, ex=3600)  # 1시간 유효
        return {
            "status": "✅ 저장 완료",
            "key": key,
            "value": value
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/cache/{key}")
def get_cache(key: str):
    """Redis에서 데이터 조회"""
    try:
        value = redis_client.get(key)
        if value:
            return {
                "status": "✅ 조회 성공",
                "key": key,
                "value": value
            }
        else:
            return {
                "status": "❌ 데이터 없음",
                "key": key
            }
    except Exception as e:
        return {"error": str(e)}, 500

@app.delete("/cache/{key}")
def delete_cache(key: str):
    """Redis에서 데이터 삭제"""
    try:
        result = redis_client.delete(key)
        return {
            "status": "✅ 삭제 완료" if result else "⚠️ 해당 키 없음",
            "key": key
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/stats")
def get_stats():
    """Redis 통계"""
    try:
        info = redis_client.info()
        return {
            "connected_clients": info.get("connected_clients"),
            "used_memory": info.get("used_memory_human"),
            "total_commands": info.get("total_commands_processed")
        }
    except Exception as e:
        return {"error": str(e)}, 500