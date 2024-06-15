import os
from typing import Union


def parse_bool(value: Union[bool, str]) -> bool:
    if isinstance(value, str):
        value = value.lower() in ("true", "1", "t")
    return value


PORT = int(os.environ.get("PORT", 8000))
POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
MINIO_ROOT_USER = os.environ.get("MINIO_ROOT_USER", "minioadmin")
MINIO_ROOT_PASSWORD = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
INTERNAL_MEDIA_SERVICE = parse_bool(os.environ.get("INTERNAL_MEDIA_SERVICE", False))
