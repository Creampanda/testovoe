from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from app import Base


class Meme(Base):
    __tablename__ = "meme"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    minio_bucket = Column(String(255), nullable=False)
    minio_path = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
