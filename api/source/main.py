from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import os
from dotenv import load_dotenv
app = FastAPI()

load_dotenv()

#connect Redis 
redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT", 6379), decode_responses=True)

#connect DB
try:
    db_conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
        port=os.getenv("POSTGRES_PORT"),
    )
    db_cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    print("Connected to DB")
except Exception as e:
    print(e)
    db_conn = None
    


@app.post("/redis/set/")
def set_key_redis(key:str, value:str, expire: int=0):
    
    try:
        if expire > 0:
            redis_client.setex(key, value, ex=expire)
        else:
            redis_client.set(key, value)
        return {"status":"add value suceess"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/redis/get/")
def get_key_redis(key:str):
    
    try:
        value = redis_client.get(key)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    return {"value": value}