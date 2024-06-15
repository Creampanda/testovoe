from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime


# Определение модели мема для ответа
class MemeResponse(BaseModel):
    """
    MemeResponse представляет собой модель данных для ответа с информацией о меме.

    Attributes:
        id (int): Уникальный идентификатор мема.
        title (str): Название мема.
        minio_bucket (str): Название бакета MinIO, в котором хранится мем.
        minio_path (str): Путь к файлу мема в бакете MinIO.
        minio_url (HttpUrl): Ссылка на файл мема.
        created_at (datetime): Время создания мема.
        updated_at (datetime): Время последнего обновления мема.
    """

    id: int
    title: str
    minio_bucket: str
    minio_path: str
    minio_url: HttpUrl
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Обобщенная модель для ответа с пагинацией
class PaginatedMemesResponse(BaseModel):
    """
    PaginatedMemesResponse представляет собой модель данных для ответа с информацией о пагинированном списке мемов.

    Attributes:
        items (List[MemeResponse]): Список мемов на текущей странице.
        total (int): Общее количество мемов.
        page (int): Номер текущей страницы.
        page_size (int): Количество мемов на странице.
    """

    items: List[MemeResponse]
    total: int
    page: int
    page_size: int
