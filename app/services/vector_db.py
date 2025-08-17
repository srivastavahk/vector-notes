from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.http import models
from app.core.config import settings
from functools import lru_cache
import uuid

class VectorDBService:
    def __init__(self, url: str, api_key: str, collection_name: str):
        self.collection_name = collection_name
        # Use Async client for FastAPI
        self.client = AsyncQdrantClient(url=url, api_key=api_key)
        self.sync_client = QdrantClient(url=url, api_key=api_key) # For initial setup

    def setup_collection(self):
        """Creates the Qdrant collection if it doesn't exist."""
        try:
            self.sync_client.get_collection(collection_name=self.collection_name)
        except Exception:
            self.sync_client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=models.Distance.COSINE
                ),
            )
            # Create a payload index on user_id for efficient filtering
            self.sync_client.create_payload_index(
                collection_name=self.collection_name,
                field_name="user_id",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )
        print(f"Qdrant collection '{self.collection_name}' is ready.")


    async def upsert_note(self, note_id: uuid.UUID, user_id: str, vector: list[float]):
        """Upserts a note's vector into the collection."""
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(note_id),
                    vector=vector,
                    payload={"user_id": user_id}
                )
            ],
            wait=True
        )

    async def search_notes(self, user_id: str, query_vector: list[float], limit: int = 5) -> list[uuid.UUID]:
        """Searches for similar notes for a specific user."""
        search_result = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id)
                    )
                ]
            ),
            limit=limit,
            with_payload=False, # We only need the IDs
        )
        return [uuid.UUID(hit.id) for hit in search_result]

    async def delete_note(self, note_id: uuid.UUID):
        """Deletes a note's vector from the collection."""
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=[str(note_id)]),
        )

@lru_cache()
def get_vector_db_service() -> VectorDBService:
    service = VectorDBService(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        collection_name=settings.QDRANT_COLLECTION_NAME
    )
    service.setup_collection()
    return service
