from pathlib import Path
from loguru import logger
from fastapi import FastAPI
from minio.commonconfig import CopySource
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from app.schemas.events import MinioEvent
from app.config.settings import settings
from app.config.s3 import client


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=None,  # Disable so that our override (below) will work
    redoc_url=None,  # Disable
)


@app.get("/", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url=str(app.openapi_url),
        title=app.title,
        swagger_js_url=settings.swagger_js_url,
        swagger_css_url=settings.swagger_css_url,
        swagger_favicon_url="/static/favicon.png",
    )


@app.get("/favicon.ico")
async def favicon():
    file_name = "favicon.png"
    return FileResponse(
        path=Path(__file__).parent / "static" / file_name,
        headers={"Content-Disposition": "attachment; filename=" + file_name},
    )


@app.get("/health", include_in_schema=False)
def healthcheck():
    return {"message": "Healthy!"}


@app.post("/minio/webhook")
def webhook(request: MinioEvent):
    for record in request.Records:
        client.copy_object(
            settings.s3_success_bucket_name,
            object_name=record.s3.object.key,
            source=CopySource(record.s3.bucket.name, record.s3.object.key),
        )
        client.remove_object(record.s3.bucket.name, record.s3.object.key)
    return {"message": "received"}


app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
