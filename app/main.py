import os
import redis
from fastapi import FastAPI

app = FastAPI(title="DevOps Demo App")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
APP_VERSION = os.getenv("APP_VERSION", "1.0.1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/")
def read_root():
    try:
        r = get_redis()
        visits = r.incr("visits_counter")
    except Exception:
        visits = "Redis offline (tryb standalone)"

    return {
        "application": "DevOps Automated Deployment Demo",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "visits": visits
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": APP_VERSION}
