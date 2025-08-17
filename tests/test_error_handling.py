from fastapi import status

def test_unauthenticated_access(test_client):
    # Remove auth override
    test_client.app.dependency_overrides = {}
    
    response = test_client.get("/api/notes")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_invalid_note_creation(test_client):
    invalid_data = {"title": "", "content": ""}  # Missing required fields
    response = test_client.post("/api/notes", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
