import sys
import os
import logging
from pydantic_settings import BaseSettings
from app.schemas.app import LogLevel
from loguru import logger


class Settings(BaseSettings):
    # app info
    app_name: str = "minio_events_handler"
    app_description: str = "Webhook server for minio bucket events"
    app_version: str = os.getenv("APP_VERSION", "0.0.1")
    log_level: LogLevel = LogLevel(os.getenv("LOG_LEVEL", "DEBUG").upper())

    # s3 object storage service info
    s3_username: str = os.getenv("S3_USERNAME", "minioadmin")
    s3_password: str = os.getenv("S3_PASSWORD", "minioadmin")
    s3_host: str = os.getenv("S3_HOST", "localhost:9000")
    s3_verify_server_cert: bool = os.getenv("S3_VERIFY_SERVER_CERT", "false").lower() == "true"
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "events")
    s3_success_bucket_name: str = os.getenv("S3_SUCCESS_BUCKET_NAME", "success")

    swagger_js_url: str = os.getenv(
        "SWAGGER_JS_URL",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    )
    swagger_css_url: str = os.getenv(
        "SWAGGER_CSS_URL",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


settings = Settings()

logger.remove(0)
logger.add(sys.stderr, level=settings.log_level)


# Filter out /health endpoint
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health") == -1


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
