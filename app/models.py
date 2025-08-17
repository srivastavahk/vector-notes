from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class User(BaseModel):
    id: str
    email: str
    created_at: datetime

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class Note(NoteCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class SearchResult(BaseModel):
    id: str
    score: float
    payload: Note
