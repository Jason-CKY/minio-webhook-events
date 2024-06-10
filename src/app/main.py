from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from app.schemas.events import MinioEvent
from app.config.settings import settings
from loguru import logger


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
async def webhook(request: MinioEvent):
    logger.critical(request.model_dump_json(indent=4))
    return {"message": "received"}


app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
