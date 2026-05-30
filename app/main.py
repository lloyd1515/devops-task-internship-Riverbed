"""Simple FastAPI app with a Redis-backed visit counter."""

import os

import redis
from fastapi import FastAPI

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = FastAPI(title="DevOps Intern Demo", version="0.1.0")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


### Backend API endpoints
@app.get("/health")
def health() -> dict:
    try:
        r.ping()
        redis_ok = True
    except redis.RedisError:
        redis_ok = False
    return {"status": "ok", "redis": redis_ok}

@app.get("/visits")
def visits() -> dict:
    count = r.incr("visits")
    return {"visits": count}