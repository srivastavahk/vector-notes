import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from app.database import Database
from app.auth import get_current_active_user
from app.models import User

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture
def mock_current_user():
    return {
        "id": "test_user_123",
        "email": "test@example.com",
        "created_at": "2023-01-01T00:00:00"
    }

@pytest.fixture(autouse=True)
def override_auth_dependency(mock_current_user):
    app.dependency_overrides[get_current_active_user] = lambda: mock_current_user
    yield
    app.dependency_overrides = {}

@pytest.fixture
def mock_db():
    with patch("app.database.Database") as mock:
        db = mock.return_value
        db.get_user_by_email.return_value = {
            "id": "test_user_123",
            "email": "test@example.com",
            "created_at": "2023-01-01T00:00:00"
        }
        db.create_note.return_value = {
            "id": "note_123",
            "user_id": "test_user_123",
            "title": "Test Note",
            "content": "This is a test note",
            "tags": ["test"],
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        db.get_note.return_value = {
            "id": "note_123",
            "user_id": "test_user_123",
            "title": "Test Note",
            "content": "This is a test note",
            "tags": ["test"],
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        db.list_notes.return_value = [{
            "id": "note_123",
            "user_id": "test_user_123",
            "title": "Test Note",
            "content": "This is a test note",
            "tags": ["test"],
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }]
        yield db

@pytest.fixture
def mock_embedding_service():
    with patch("app.embeddings.EmbeddingService") as mock:
        service = mock.return_value
        service.generate_embedding.return_value = [0.1, 0.2, 0.3] * 512  # 1536-dim vector
        yield service

@pytest.fixture
def mock_vector_db():
    with patch("app.vector_db.VectorDB") as mock:
        vector_db = mock.return_value
        vector_db.search_similar.return_value = [
            {
                "id": "note_123",
                "score": 0.85,
                "payload": {
                    "title": "Test Note",
                    "content": "This is a test note",
                    "tags": ["test"],
                    "user_id": "test_user_123"
                }
            }
        ]
        yield vector_db# Basic test for user logic
