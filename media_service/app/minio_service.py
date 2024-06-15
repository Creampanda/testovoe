import logging
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
        self.ensure_bucket_exists("models")
        self.ensure_bucket_exists("datasets")

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

    def add_file(self, bucket_name, object_name, file_path):
        # Upload a file to the specified bucket.
        try:
            result = self.client.fput_object(bucket_name, object_name, file_path)
            logger.info(f"File '{file_path}' uploaded as '{object_name}' to bucket '{bucket_name}'.")
            return result
        except S3Error as e:
            logger.error(f"Failed to upload file: {e}")

    def get_file(self, bucket_name, object_name, file_path):
        # Download a file from the specified bucket.
        try:
            result = self.client.fget_object(bucket_name, object_name, file_path)
            logger.info(f"File '{object_name}' downloaded from bucket '{bucket_name}' to '{file_path}'.")
            return result
        except S3Error as e:
            logger.error(f"Failed to download file: {e}")
