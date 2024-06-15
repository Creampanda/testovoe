import logging
from fastapi import HTTPException, status
from minio import Minio
from minio.error import S3Error
from app.config import MINIO_ROOT_USER, MINIO_ROOT_PASSWORD

logger = logging.getLogger("resources")


class MinioService:
    def __init__(self):
        # Initialize minio client with an endpoint and access/secret keys.
        self.client = Minio(
            endpoint="minio:9000",
            access_key=MINIO_ROOT_USER,
            secret_key=MINIO_ROOT_PASSWORD,
            secure=False,  # Set to True if you use https
        )
        self.ensure_bucket_exists("memes")

    def ensure_bucket_exists(self, bucket_name):
        # Create a bucket if it does not exist.
        try:
            found = self.client.bucket_exists(bucket_name)
            if not found:
                self.client.make_bucket(bucket_name)
                logger.info(f"Bucket '{bucket_name}' created successfully.")
            else:
                logger.info(f"Bucket '{bucket_name}' already exists.")
        except S3Error as e:
            logger.error(f"An error occurred while checking/creating the bucket: {e}")

    def get_presigned_url(self, bucket_name, object_name):
        # Generate a presigned URL to access the object
        try:
            presigned_url = self.client.presigned_get_object(bucket_name, object_name)
            logger.info(f"Presigned URL for '{object_name}' in bucket '{bucket_name}' is generated.")
            return presigned_url
        except S3Error as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            return None

    def upload_to_minio(self, bucket_name: str, minio_path: str, file_data: str) -> str:
        try:
            self.client.put_object(bucket_name, minio_path, file_data, length=-1, part_size=10 * 1024 * 1024)
            return minio_path
        except S3Error as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
