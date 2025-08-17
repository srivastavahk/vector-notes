from fastapi import status

def test_semantic_search(test_client, mock_embedding_service, mock_vector_db):
    response = test_client.get("/api/search?query=test+note")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "note_123"
    assert data[0]["score"] == 0.85
    
    # Verify embedding generation was called
    mock_embedding_service.generate_embedding.assert_called_with("test note")

def test_search_missing_query(test_client):
    response = test_client.get("/api/search")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_search_limit_parameter(test_client, mock_vector_db):
    response = test_client.get("/api/search?query=test&limit=3")
    assert response.status_code == status.HTTP_200_OK
    mock_vector_db.search_similar.assert_called_with(
        "test_user_123", 
        [0.1, 0.2, 0.3] * 512,  # Mocked embedding
        3
    )
