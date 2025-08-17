import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.models.note import NoteCreate, NoteUpdate, NoteSchema
from app.services.note_service import NoteService
from app.api.deps import get_current_user, get_supabase_client
from app.services.ai_services import get_ai_service, AIService
from app.services.vector_db import get_vector_db_service, VectorDBService
from supabase import Client

router = APIRouter(prefix="/notes", tags=["Notes"])

def get_note_service(
    db: Client = Depends(get_supabase_client),
    ai: AIService = Depends(get_ai_service),
    vector_db: VectorDBService = Depends(get_vector_db_service)
) -> NoteService:
    return NoteService(db, ai, vector_db)

@router.post("/", response_model=NoteSchema, status_code=status.HTTP_201_CREATED)
async def create_new_note(
    note_in: NoteCreate,
    service: NoteService = Depends(get_note_service),
    current_user = Depends(get_current_user)
):
    """Create a new note. The title is auto-generated."""
    note = await service.create_note(note_in, user_id=current_user.id)
    return note

@router.get("/search", response_model=List[NoteSchema])
async def search_notes_by_query(
    q: str = Query(..., min_length=3, description="Natural language search query"),
    service: NoteService = Depends(get_note_service),
    current_user = Depends(get_current_user)
):
    """Retrieve notes based on semantic similarity to a natural language query."""
    return await service.search_user_notes(query=q, user_id=current_user.id)

@router.get("/", response_model=List[NoteSchema])
def get_all_user_notes(
    page: int = 1,
    page_size: int = 20,
    service: NoteService = Depends(get_note_service),
    current_user = Depends(get_current_user)
):
    """Retrieve all notes for the authenticated user with pagination."""
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="Page and page_size must be positive.")
    return service.get_all_notes(user_id=current_user.id, page=page, page_size=page_size)

@router.get("/{note_id}", response_model=NoteSchema)
async def get_note(
    note_id: uuid.UUID,
    service: NoteService = Depends(get_note_service),
    current_user = Depends(get_current_user)
):
    """Retrieve a specific note by its ID."""
    note = await service.get_note_by_id(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteSchema)
async def update_existing_note(
    note_id: uuid.UUID,
    note_in: NoteUpdate,
    service: NoteService = Depends(get_note_service),
    current_user = Depends(get_current_user)
):
    """Update a note's content or tags."""
    updated_note = await service.update_note(note_id, note_in, current_user.id)
    if not updated_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_note(
    note_id: uuid.UUID,
    service: NoteService = Depends(get_note_service),
    current_user = Depends(get_current_user)
):
    """Delete a note by its ID."""
    success = await service.delete_note(note_id, current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
