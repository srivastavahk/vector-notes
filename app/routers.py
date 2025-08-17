from fastapi import APIRouter, Depends, HTTPException, status
from app.models import NoteCreate, NoteUpdate, Note, SearchResult
from app.services import NoteService, SearchService
from app.auth import get_current_active_user

router = APIRouter()

@router.post("/notes", response_model=Note, status_code=201)
async def create_note(
    note: NoteCreate,
    current_user: dict = Depends(get_current_active_user)
):
    return NoteService.create_note(current_user['id'], note)

@router.get("/notes", response_model=list[Note])
async def list_notes(
    current_user: dict = Depends(get_current_active_user)
):
    return NoteService.list_notes(current_user['id'])

@router.get("/notes/{note_id}", response_model=Note)
async def get_note(
    note_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    note = NoteService.get_note(note_id, current_user['id'])
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    updated_note = NoteService.update_note(note_id, current_user['id'], note_update)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note

@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    NoteService.delete_note(note_id, current_user['id'])
    return {}

@router.get("/search", response_model=list[SearchResult])
async def semantic_search(
    query: str,
    limit: int = 5,
    current_user: dict = Depends(get_current_active_user)
):
    return SearchService.semantic_search(current_user['id'], query, limit)
