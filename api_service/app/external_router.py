from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.minio_service import MinioService
from app.services.meme_service import MemeService
from app import get_db, get_minio_service
from app.models.meme_responses import PaginatedMemesResponse

router = APIRouter()

@router.get("/memes", response_model=PaginatedMemesResponse)
async def get_memes(
    page: int = Query(default=1, gt=0, description="Номер страницы."),
    page_size: int = Query(default=10, gt=0, le=100, description="Количество мемов на странице."),
    db: Session = Depends(get_db),
    minio_service: MinioService = Depends(get_minio_service),
):
    """
    Получение списка мемов с пагинацией.

    Args:
        page (int): Номер страницы. По умолчанию 1.
        page_size (int): Количество мемов на странице. По умолчанию 10. Максимум 100.
        db (Session): Сессия базы данных, автоматически внедряемая FastAPI.
        minio_service (MinioService): Клиент MinIO для работы с файловым хранилищем, автоматически внедряемый FastAPI.

    Returns:
        PaginatedMemesResponse: Объект ответа с пагинированными мемами.

    Raises:
        HTTPException: Если произошла ошибка при получении мемов.
    """
    try:
        meme_service = MemeService(db, minio_service)
        return meme_service.get_paginated_memes(page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
