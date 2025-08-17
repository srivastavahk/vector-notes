# import google.generativeai as genai
# from app.core.config import settings
# from functools import lru_cache
# import asyncio

# # Configure the Gemini client
# genai.configure(api_key=settings.GOOGLE_API_KEY)

# class AIService:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         if not self.api_key:
#             raise ValueError("Google API key is not configured.")

#     async def generate_embedding(self, text: str) -> list[float]:
#         """Generates embedding for a given text."""
#         try:
#             result = await asyncio.to_thread(
#                 genai.embed_content,
#                 model=settings.EMBEDDING_MODEL,
#                 content=text,
#                 task_type="RETRIEVAL_DOCUMENT"
#             )
#             return result['embedding']
#         except Exception as e:
#             # Handle potential API errors
#             print(f"Error generating embedding: {e}")
#             raise

#     async def generate_title_from_content(self, content: str) -> str:
#         """Generates a concise title from note content."""
#         try:
#             model = genai.GenerativeModel('gemini-1.5-flash')
#             prompt = f"Generate a very concise title (5 words or less, no markdown) for the following note content: '{content[:500]}'"
#             response = await model.generate_content_async(prompt)
#             # Clean up the response
#             return response.text.strip().replace("*", "").replace("\n", "")
#         except Exception as e:
#             print(f"Error generating title: {e}")
#             # Fallback title
#             return "Untitled Note"

# @lru_cache()
# def get_ai_service() -> AIService:
#     return AIService(api_key=settings.GOOGLE_API_KEY)

from functools import lru_cache
import httpx
from app.core.config import settings

class AIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.jina.ai/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_embedding(self, text: str) -> list[float]:
        """Generates embedding for a given text using Jina AI's API."""
        if not text.strip():
            return [0.0] * settings.EMBEDDING_DIMENSION

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                payload = {
                    "input": [text], # Jina API expects a list of strings
                    "model": settings.JINA_EMBEDDING_MODEL
                }
                response = await client.post(self.api_url, headers=self.headers, json=payload)
                response.raise_for_status()

                # Extract the embedding from the response structure
                data = response.json()
                return data["data"][0]["embedding"]

            except httpx.HTTPStatusError as e:
                print(f"HTTP error calling Jina AI API: {e.response.text}")
                raise
            except (KeyError, IndexError) as e:
                print(f"Error parsing Jina AI API response: {e}")
                raise
            except Exception as e:
                print(f"An error occurred while generating embedding: {e}")
                raise

    async def generate_title_from_content(self, content: str) -> str:
        """Generates a simple title from the content, efficiently."""
        words = content.strip().split(maxsplit=5)
        if not words:
            return "Untitled Note"
        title = " ".join(words[:5])
        if len(words) > 5:
            title += "..."
        return title

# Dependency provider for the AIService
@lru_cache()
def get_ai_service() -> AIService:
    if not settings.JINA_API_KEY:
        raise ValueError("Jina AI API Key is not configured.")
    return AIService(api_key=settings.JINA_API_KEY)
