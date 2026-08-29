
from io import BytesIO

from minio import Minio

from app.core.config import settings


class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False,
        )

    def ensure_bucket(self, bucket_name: str) -> None:
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        data: bytes,
        content_type: str,
    ) -> str:
        self.ensure_bucket(bucket_name)

        self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=BytesIO(data),
            length=len(data),
            content_type=content_type,
        )

        return f"s3://{bucket_name}/{object_name}"


storage = StorageService()

