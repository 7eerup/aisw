import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

PORT = int(os.getenv("PORT", 8000))
MODE = os.getenv("MODE", "development")

@app.get("/")
def read_root():
    return {"message": "Hello", "mode": MODE, "port": PORT}

@app.get("/status")
def status():
    return {"status": "running", "mode": MODE}

# 이 부분 추가!
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)