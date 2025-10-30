import os
from pydantic_settings import BaseSettings

# Load .env file if it exists (for local development)
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # Rate Limiting
    RATE_LIMIT: str = "10/minute"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str

    # Qdrant Vector DB
    QDRANT_URL: str
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "vectornotes"

    # Google Gemini API
    #GOOGLE_API_KEY: str

    # Jina AI API Key
    JINA_API_KEY: str
    EMBEDDING_MODEL: str

    # Embedding model configuration
    # EMBEDDING_MODEL: str = "models/text-embedding-004"
    EMBEDDING_DIMENSION: int = 1024

    class Config:
        case_sensitive = True

def get_settings() -> Settings:
    return Settings()

settings = get_settings()
