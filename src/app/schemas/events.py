from pydantic import BaseModel
from typing import List

class MinioS3ObjectRecord(BaseModel):
    key: str
    size: int
    eTag: str
    contentType: str


class MinioS3BucketRecord(BaseModel):
    name: str
    arn: str


class MinioS3EventRecord(BaseModel):
    s3SchemaVersion: str
    configurationId: str
    bucket: MinioS3BucketRecord
    object: MinioS3ObjectRecord


class MinioEventRecord(BaseModel):
    s3: MinioS3EventRecord


class MinioEvent(BaseModel):
    EventName: str
    Key: str
    Records: List[MinioEventRecord]

