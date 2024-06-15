from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.message_response import MessageResponse
from app.models.meme_responses import PaginatedMemesResponse, MemeResponse
from app.minio_service import MinioService
from app.services.meme_service import MemeService
from app import get_db, get_minio_service

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


@router.get("/memes/{id}", response_model=MemeResponse)
async def get_meme(
    id: int, db: Session = Depends(get_db), minio_service: MinioService = Depends(get_minio_service)
):
    """
    Получение мема по его идентификатору.

    Args:
        id (int): Идентификатор мема.
        db (Session): Сессия базы данных, автоматически внедряемая FastAPI.
        minio_service (MinioService): Клиент MinIO для работы с файловым хранилищем, автоматически внедряемый FastAPI.

    Returns:
        MemeResponse: Объект ответа с информацией о меме.

    Raises:
        HTTPException: Если мем не найден.
    """
    try:
        meme_service = MemeService(db, minio_service)
        meme = meme_service.get_meme_by_id(id)
        if not meme:
            raise HTTPException(status_code=404, detail="Meme not found")
        return meme
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/memes", response_model=MemeResponse)
async def create_meme(
    title: str = Form(..., description="Название мема."),
    file: UploadFile = File(..., description="Файл изображения мема."),
    db: Session = Depends(get_db),
    minio_service: MinioService = Depends(get_minio_service),
):
    """
    Создание нового мема.

    Args:
        title (str): Название мема.
        file (UploadFile): Файл изображения мема.
        db (Session): Сессия базы данных, автоматически внедряемая FastAPI.
        minio_service (MinioService): Клиент MinIO для работы с файловым хранилищем, автоматически внедряемый FastAPI.

    Returns:
        MemeResponse: Объект ответа с информацией о созданном меме.

    Raises:
        HTTPException: Если произошла ошибка при создании мема.
    """
    try:
        meme_service = MemeService(db, minio_service)
        meme = meme_service.create_meme(title, file)
        return meme
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/memes/{id}", response_model=MemeResponse)
async def update_meme(
    id: int,
    title: str = Form(..., description="Новое название мема."),
    file: UploadFile = File(None, description="Новый файл изображения мема."),
    db: Session = Depends(get_db),
    minio_service: MinioService = Depends(get_minio_service),
):
    """
    Обновление существующего мема.

    Args:
        id (int): Идентификатор мема.
        title (str): Новое название мема.
        file (UploadFile, optional): Новый файл изображения мема.
        db (Session): Сессия базы данных, автоматически внедряемая FastAPI.
        minio_service (MinioService): Клиент MinIO для работы с файловым хранилищем, автоматически внедряемый FastAPI.

    Returns:
        MemeResponse: Объект ответа с информацией о меме.

    Raises:
        HTTPException: Если мем не найден или произошла ошибка при обновлении мема.
    """
    try:
        meme_service = MemeService(db, minio_service)
        meme = meme_service.update_meme(id, title, file)
        if not meme:
            raise HTTPException(status_code=404, detail="Meme not found")
        return meme
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memes/{id}", response_model=MessageResponse)
async def delete_meme(
    id: int, db: Session = Depends(get_db), minio_service: MinioService = Depends(get_minio_service)
):
    """
    Удаление мема по его идентификатору.

    Args:
        id (int): Идентификатор мема.
        db (Session): Сессия базы данных, автоматически внедряемая FastAPI.
        minio_service (MinioService): Клиент MinIO для работы с файловым хранилищем, автоматически внедряемый FastAPI.

    Returns:
        MessageResponse: Объект ответа с сообщением об успешном удалении мема.

    Raises:
        HTTPException: Если мем не найден или произошла ошибка при удалении мема.
    """
    try:
        meme_service = MemeService(db, minio_service)
        success = meme_service.delete_meme(id)
        if not success:
            raise HTTPException(status_code=404, detail="Meme not found")
        return MessageResponse(message="Meme deleted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
