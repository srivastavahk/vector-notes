from fastapi import APIRouter
from app.modules.users.api import router as user_router
from app.modules.notes.api import router as notes_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(notes_router, prefix="/notes", tags=["Notes"])
