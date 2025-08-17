from fastapi import FastAPI
from app.routers import router
from app.config import settings
import uvicorn

app = FastAPI(
    title="Notes API",
    description="Secure notes application with semantic search",
    version="0.1.0"
)

app.include_router(router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
