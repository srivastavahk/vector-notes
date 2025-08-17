from fastapi import HTTPException, status
from app.auth import get_current_active_user
from app.database import Database

def test_valid_token(monkeypatch):
    mock_user = {"id": "user_123", "email": "test@example.com"}
    monkeypatch.setattr(Database, "get_user_by_email", lambda *args, **kwargs: mock_user)

    # Mock JWT decode
    class MockPayload:
        def get(self, key):
            return "test@example.com"

    with patch("app.auth.jwt.decode", return_value=MockPayload()):
        user = get_current_active_user("valid_token")
        assert user["email"] == "test@example.com"

def test_invalid_token():
    with patch("app.auth.jwt.decode", side_effect=Exception("Invalid token")):
        try:
            get_current_active_user("invalid_token")
            assert False, "Should have raised exception"
        except HTTPException as e:
            assert e.status_code == status.HTTP_401_UNAUTHORIZED

def test_user_not_found(monkeypatch):
    monkeypatch.setattr(Database, "get_user_by_email", lambda *args, **kwargs: None)

    # Mock JWT decode
    class MockPayload:
        def get(self, key):
            return "test@example.com"

    with patch("app.auth.jwt.decode", return_value=MockPayload()):
        try:
            get_current_active_user("valid_token")
            assert False, "Should have raised exception"
        except HTTPException as e:
            assert e.status_code == status.HTTP_401_UNAUTHORIZED
