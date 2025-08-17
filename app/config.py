from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: "https://wcobsxmcluqnyebhgixj.supabase.co"
    supabase_key: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indjb2JzeG1jbHVxbnllYmhnaXhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUzNDU0NjYsImV4cCI6MjA3MDkyMTQ2Nn0.WI4IB10ViprJ3yxlpyo4tE5UClKHWnSPrRO5ZQ22vl8"
    openai_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    embedding_model: str = "text-embedding-ada-002"
    jwt_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
