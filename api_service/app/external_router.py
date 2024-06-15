from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.minio_service import MinioService
from app.services.meme_service import MemeService
from app import get_db, get_minio_service
from app.models.meme_responses import PaginatedMemesResponse

router = APIRouter()


@router.get("/memes", response_model=PaginatedMemesResponse)
async def get_memes(
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
    db: Session = Depends(get_db),
    minio_service: MinioService = Depends(get_minio_service),
):
    meme_service = MemeService(db, minio_service)
    return meme_service.get_paginated_memes(page, page_size)
