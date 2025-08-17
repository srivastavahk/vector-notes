import openai
from app.config import settings

openai.api_key = settings.openai_api_key

class EmbeddingService:
    @staticmethod
    def generate_embedding(text: str) -> list[float]:
        response = openai.Embedding.create(
            input=text,
            model=settings.embedding_model
        )
        return response['data'][0]['embedding']
