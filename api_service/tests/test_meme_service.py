import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app import get_db, get_minio_service, Base
from app.minio_service import MinioService
from app.services.meme_service import MemeService
from unittest.mock import MagicMock
from fastapi import UploadFile
from io import BytesIO
from starlette.datastructures import Headers

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_minio_service():
    minio_client = MagicMock()
    minio_client.get_presigned_url.return_value = "http://localhost:9000/mocked_url"
    minio_service = MinioService(client=minio_client)
    return minio_service

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_minio_service] = override_get_minio_service

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    yield client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def minio_service():
    minio_service = MagicMock()
    minio_service.get_presigned_url.return_value = "http://localhost:9000/mocked_url"
    return minio_service

@pytest.fixture
def meme_service(db_session, minio_service):
    return MemeService(db_session, minio_service)

def test_create_meme(meme_service):
    with open("api_service/tests/fixtures/test_image.jpg", "rb") as f:
        file_content = f.read()
    headers = Headers({"content-type": "image/jpeg"})
    file = UploadFile(filename="test_image.jpg", file=BytesIO(file_content), headers=headers)
    meme_response = meme_service.create_meme("Test Meme", file)
    assert meme_response.title == "Test Meme"
    assert meme_response.minio_path.endswith(".jpg")

def test_get_paginated_memes(meme_service):
    response = meme_service.get_paginated_memes(1, 10)
    assert response.page == 1
    assert response.page_size == 10
    assert isinstance(response.items, list)

def test_get_meme_by_id(meme_service):
    with open("api_service/tests/fixtures/test_image.jpg", "rb") as f:
        file_content = f.read()
    headers = Headers({"content-type": "image/jpeg"})
    file = UploadFile(filename="test_image.jpg", file=BytesIO(file_content), headers=headers)
    created_meme = meme_service.create_meme("Test Meme", file)
    meme_response = meme_service.get_meme_by_id(created_meme.id)
    assert meme_response.id == created_meme.id
    assert meme_response.title == "Test Meme"

def test_update_meme(meme_service):
    with open("api_service/tests/fixtures/test_image.jpg", "rb") as f:
        file_content = f.read()
    headers = Headers({"content-type": "image/jpeg"})
    file = UploadFile(filename="test_image.jpg", file=BytesIO(file_content), headers=headers)
    created_meme = meme_service.create_meme("Test Meme", file)

    with open("api_service/tests/fixtures/test_image.jpg", "rb") as f:
        updated_file_content = f.read()
    updated_headers = Headers({"content-type": "image/jpeg"})
    updated_file = UploadFile(filename="updated_test_image.jpg", file=BytesIO(updated_file_content), headers=updated_headers)
    updated_meme_response = meme_service.update_meme(created_meme.id, "Updated Test Meme", updated_file)
    assert updated_meme_response.title == "Updated Test Meme"
    assert updated_meme_response.minio_path.endswith(".jpg")

def test_delete_meme(meme_service):
    with open("api_service/tests/fixtures/test_image.jpg", "rb") as f:
        file_content = f.read()
    headers = Headers({"content-type": "image/jpeg"})
    file = UploadFile(filename="test_image.jpg", file=BytesIO(file_content), headers=headers)
    created_meme = meme_service.create_meme("Test Meme", file)

    success = meme_service.delete_meme(created_meme.id)
    assert success is True
    meme_response = meme_service.get_meme_by_id(created_meme.id)
    assert meme_response is None
