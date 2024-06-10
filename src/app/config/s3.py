from app.config.settings import settings
from minio import Minio


client = Minio(
    endpoint=settings.s3_host,
    access_key=settings.s3_username,
    secret_key=settings.s3_password,
    secure=settings.s3_verify_server_cert,
    region="Singapore",
    cert_check=True,
)
