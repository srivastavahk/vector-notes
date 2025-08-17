from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.routers import notes
from app.core.config import settings

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])

def create_app() -> FastAPI:
    app = FastAPI(
        title="Notes Management API",
        description="A scalable and secure API for managing and searching user notes.",
        version="1.0.0"
    )

    # Add middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add rate limiting state and handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add routers
    app.include_router(notes.router)

    @app.get("/", tags=["Health Check"])
    def read_root():
        return {"status": "ok", "message": "Welcome to the Notes API!"}

    return app

app = create_app()
