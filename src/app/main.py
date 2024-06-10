from fastapi import FastAPI
from app.schemas.events import MinioEvent
from loguru import logger

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/minio/webhook")
async def webhook(request: MinioEvent):
    logger.critical(request.model_dump_json(indent=4))
    return {"message": "received"}
