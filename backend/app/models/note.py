import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class NoteBase(BaseModel):
    content: str
    tags: Optional[List[str]] = []

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class NoteSchema(NoteBase):
    id: uuid.UUID = Field(..., alias="id")
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
