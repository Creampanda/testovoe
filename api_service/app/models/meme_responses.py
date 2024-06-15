from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Определение модели мема для ответа
class MemeResponse(BaseModel):
    id: int
    title: str
    minio_bucket: str
    minio_path: str
    minio_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Обобщенная модель для ответа с пагинацией
class PaginatedMemesResponse(BaseModel):
    items: List[MemeResponse]
    total: int
    page: int
    page_size: int
