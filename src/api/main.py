import json
from fastapi import FastAPI, Request
from minio import Minio
from loguru import logger
from pydantic import BaseModel
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/minio/webhook")
async def webhook(request: Request):
    body = await request.json()
    logger.critical(json.dumps(body, indent=4))
    return {"message": "received"}
