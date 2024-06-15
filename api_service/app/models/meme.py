from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

from app import Base

class Meme(Base):
    """
    Meme представляет собой модель данных для хранения информации о меме.

    Attributes:
        id (int): Уникальный идентификатор мема.
        title (str): Название мема.
        minio_bucket (str): Название бакета MinIO, в котором хранится мем.
        minio_path (str): Путь к файлу мема в бакете MinIO.
        created_at (datetime): Время создания мема.
        updated_at (datetime): Время последнего обновления мема.
    """
    __tablename__ = "meme"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    minio_bucket = Column(String(255), nullable=False)
    minio_path = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @validates('title')
    def validate_title(self, key, value):
        """
        Валидация названия мема. Название не должно быть пустым и должно быть строкой.

        Args:
            key (str): Название поля.
            value (str): Значение поля.

        Returns:
            str: Провалидированное значение поля.
        
        Raises:
            ValueError: Если значение поля не соответствует требованиям.
        """
        if not value:
            raise ValueError("Title must not be empty.")
        if not isinstance(value, str):
            raise ValueError("Title must be a string.")
        return value

    @validates('minio_bucket')
    def validate_minio_bucket(self, key, value):
        """
        Валидация названия бакета MinIO. Название не должно быть пустым и должно быть строкой.

        Args:
            key (str): Название поля.
            value (str): Значение поля.

        Returns:
            str: Провалидированное значение поля.
        
        Raises:
            ValueError: Если значение поля не соответствует требованиям.
        """
        if not value:
            raise ValueError("Minio bucket must not be empty.")
        if not isinstance(value, str):
            raise ValueError("Minio bucket must be a string.")
        return value

    @validates('minio_path')
    def validate_minio_path(self, key, value):
        """
        Валидация пути к файлу мема в бакете MinIO. Путь не должен быть пустым и должен быть строкой.

        Args:
            key (str): Название поля.
            value (str): Значение поля.

        Returns:
            str: Провалидированное значение поля.
        
        Raises:
            ValueError: Если значение поля не соответствует требованиям.
        """
        if not value:
            raise ValueError("Minio path must not be empty.")
        if not isinstance(value, str):
            raise ValueError("Minio path must be a string.")
        return value
