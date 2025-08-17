from fastapi import status
from app.models import NoteCreate, NoteUpdate

def test_create_note(test_client, mock_db, mock_embedding_service, mock_vector_db):
    note_data = {
        "title": "Test Note",
        "content": "This is a test note",
        "tags": ["test"]
    }

    response = test_client.post("/api/notes", json=note_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"

    # Verify embedding generation was called
    mock_embedding_service.generate_embedding.assert_called_with("Test Note This is a test note")

    # Verify vector upsert
    mock_vector_db.upsert_vector.assert_called()

def test_get_note(test_client, mock_db):
    response = test_client.get("/api/notes/note_123")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == "note_123"

def test_get_note_not_found(test_client, mock_db):
    mock_db.get_note.return_value = None
    response = test_client.get("/api/notes/non_existent_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_notes(test_client, mock_db):
    response = test_client.get("/api/notes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "note_123"

def test_update_note(test_client, mock_db, mock_embedding_service, mock_vector_db):
    update_data = {"title": "Updated Title"}
    response = test_client.put("/api/notes/note_123", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"

    # Verify embedding update was called
    mock_embedding_service.generate_embedding.assert_called()

def test_update_note_not_found(test_client, mock_db):
    mock_db.update_note.return_value = None
    response = test_client.put("/api/notes/non_existent_id", json={"title": "Updated"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_note(test_client, mock_db, mock_vector_db):
    response = test_client.delete("/api/notes/note_123")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify vector deletion
    mock_vector_db.delete_vector.assert_called_with("note_123")
