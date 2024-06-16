from typing import Optional
import uuid
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException, UploadFile, status
import logging
from minio.error import S3Error
from app.minio_service import MinioService
from app.models.meme import Meme
from app.models.meme_responses import MemeResponse, PaginatedMemesResponse

logger = logging.getLogger("resources")


class MemeService:
    def __init__(self, db: Session, minio_client: MinioService):
        """
        Инициализация MemeService с подключением к базе данных и MinIO.

        Args:
            db (Session): Сессия базы данных.
            minio_client (MinioService): Клиент MinIO для работы с файловым хранилищем.
        """
        self.db = db
        self.minio_client = minio_client
        self.bucket_name = "memes"

    def _is_allowed_image_file(self, file: UploadFile) -> bool:
        """
        Проверка, является ли файл допустимым изображением (PNG, JPG, GIF).

        Args:
            file (UploadFile): Загруженный файл.

        Returns:
            bool: True, если файл допустим, иначе False.
        """
        allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            return False

        allowed_mime_types = {"image/png", "image/jpeg", "image/gif"}
        if file.content_type not in allowed_mime_types:
            return False

        return True

    def get_paginated_memes(self, page: int, page_size: int) -> PaginatedMemesResponse:
        """
        Получение списка мемов с пагинацией.

        Args:
            page (int): Номер страницы.
            page_size (int): Количество мемов на странице.

        Returns:
            PaginatedMemesResponse: Объект ответа с пагинированными мемами.
        """
        offset = (page - 1) * page_size
        total = self.db.query(Meme).count()
        memes = self.db.query(Meme).offset(offset).limit(page_size).all()
        memes_response = []
        for meme in memes:
            meme_data = MemeResponse(
                id=meme.id,
                title=meme.title,
                minio_bucket=meme.minio_bucket,
                minio_path=meme.minio_path,
                minio_url=self.minio_client.get_presigned_url(meme.minio_bucket, meme.minio_path),
                created_at=meme.created_at,
                updated_at=meme.updated_at,
            )
            memes_response.append(meme_data)

        return PaginatedMemesResponse(items=memes_response, total=total, page=page, page_size=page_size)

    def create_meme(self, title: str, file: UploadFile) -> MemeResponse:
        """
        Создание нового мема с загрузкой изображения в MinIO.

        Args:
            title (str): Название мема.
            file (UploadFile): Файл изображения.

        Returns:
            MemeResponse: Объект ответа с информацией о созданном меме.

        Raises:
            HTTPException: Если файл не загружен или имеет недопустимый формат.
        """
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded.")

        if not self._is_allowed_image_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only PNG, JPG, and GIF are allowed.",
            )

        file_extension = file.filename.split(".")[-1].lower()
        minio_path = f"{uuid.uuid4()}.{file_extension}"
        try:
            # Upload file to MinIO
            self.minio_client.upload_to_minio(
                bucket_name=self.bucket_name, minio_path=minio_path, file_data=file.file
            )

            # Add meme metadata to the database
            meme = Meme(
                title=title,
                minio_bucket=self.bucket_name,
                minio_path=minio_path,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            self.db.add(meme)
            self.db.commit()
            self.db.refresh(meme)

            # Generate presigned URL for the uploaded image
            presigned_url = self.minio_client.get_presigned_url(meme.minio_bucket, meme.minio_path)
            return MemeResponse(
                id=meme.id,
                title=meme.title,
                minio_bucket=meme.minio_bucket,
                minio_path=meme.minio_path,
                minio_url=presigned_url,
                created_at=meme.created_at,
                updated_at=meme.updated_at,
            )
        except S3Error as e:
            logger.error(f"Failed to upload file to MinIO: {e}")
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")

    def get_meme_by_id(self, id: int) -> Optional[MemeResponse]:
        """
        Получение мема по его идентификатору.

        Args:
            id (int): Идентификатор мема.

        Returns:
            Optional[MemeResponse]: Объект ответа с информацией о меме или None, если мем не найден.
        """
        meme = self.db.query(Meme).filter(Meme.id == id).first()
        if meme:
            presigned_url = self.minio_client.get_presigned_url(meme.minio_bucket, meme.minio_path)
            return MemeResponse(
                id=meme.id,
                title=meme.title,
                minio_bucket=meme.minio_bucket,
                minio_path=meme.minio_path,
                minio_url=presigned_url,
                created_at=meme.created_at,
                updated_at=meme.updated_at,
            )
        return None

    def update_meme(self, id: int, title: str, file: UploadFile = None) -> Optional[MemeResponse]:
        """
        Обновление существующего мема.

        Args:
            id (int): Идентификатор мема.
            title (str): Новое название мема.
            file (UploadFile, optional): Новый файл изображения.

        Returns:
            Optional[MemeResponse]: Объект ответа с информацией о меме или None, если мем не найден.
        """
        meme = self.db.query(Meme).filter(Meme.id == id).first()
        if not meme:
            return None
        if title:
            meme.title = title
        if file:
            if not self._is_allowed_image_file(file):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file type. Only PNG, JPG, and GIF are allowed.",
                )

            file_extension = file.filename.split(".")[-1].lower()
            minio_path = f"{uuid.uuid4()}.{file_extension}"
            self.minio_client.upload_to_minio(bucket_name="memes", minio_path=minio_path, file_data=file.file)
            meme.minio_path = minio_path
        meme.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(meme)
        presigned_url = self.minio_client.get_presigned_url(meme.minio_bucket, meme.minio_path)
        return MemeResponse(
            id=meme.id,
            title=meme.title,
            minio_bucket=meme.minio_bucket,
            minio_path=meme.minio_path,
            minio_url=presigned_url,
            created_at=meme.created_at,
            updated_at=meme.updated_at,
        )

    def delete_meme(self, id: int) -> bool:
        """
        Удаление мема по его идентификатору и удаление соответствующего файла из MinIO.

        Args:
            id (int): Идентификатор мема.

        Returns:
            bool: True, если мем был успешно удален, иначе False.
        """
        meme = self.db.query(Meme).filter(Meme.id == id).first()
        if not meme:
            return False
        try:
            # Удаление файла из MinIO
            self.minio_client.client.remove_object(meme.minio_bucket, meme.minio_path)
        except S3Error as e:
            logger.error(f"Failed to delete file from MinIO: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete file from storage")
        self.db.delete(meme)
        self.db.commit()
        return True
