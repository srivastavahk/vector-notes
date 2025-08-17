from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import settings

class VectorDB:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = "notes_vectors"
        self._initialize_collection()

    def _initialize_collection(self):
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # OpenAI embedding size
                    distance=models.Distance.COSINE
                )
            )

    def upsert_vector(self, note_id: str, user_id: str, vector: list[float], payload: dict):
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=note_id,
                    vector=vector,
                    payload={
                        "user_id": user_id,
                        **payload
                    }
                )
            ]
        )

    def search_similar(self, user_id: str, vector: list[float], limit: int = 5) -> list:
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id)
                ]
            ),
            limit=limit
        )
        return [
            {
                "id": result.id,
                "score": result.score,
                "payload": result.payload
            } for result in results
        ]

    def delete_vector(self, note_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[note_id]
            )
        )
