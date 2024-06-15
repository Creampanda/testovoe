from sqlalchemy.orm import Session
from minio.error import S3Error
from app.minio_service import MinioService
from app.models.meme import Meme
from app.models.meme_responses import MemeResponse, PaginatedMemesResponse


class MemeService:
    def __init__(self, db: Session, minio_client: MinioService):
        self.db = db
        self.minio_client = minio_client

    def get_paginated_memes(self, page: int, page_size: int):
        offset = (page - 1) * page_size
        total = self.db.query(Meme).count()
        memes = self.db.query(Meme).offset(offset).limit(page_size).all()
        memes_response = []
        for meme in memes:
            # Create MemeResponse object
            meme_data = MemeResponse(
                id=meme.id,
                title=meme.title,
                minio_bucket=meme.minio_bucket,
                minio_path=meme.minio_path,
                minio_url=MinioService().get_presigned_url(meme.minio_bucket, meme.minio_path),
                created_at=meme.created_at,
                updated_at=meme.updated_at,
            )
            memes_response.append(meme_data)

        return PaginatedMemesResponse(items=memes_response, total=total, page=page, page_size=page_size)
