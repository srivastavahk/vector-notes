import uuid
from supabase import Client
from app.models.note import NoteCreate, NoteUpdate
from app.services.ai_services import AIService
from app.services.vector_db import VectorDBService

class NoteService:
    def __init__(self, db: Client, ai: AIService, vector_db: VectorDBService):
        self.db = db
        self.ai = ai
        self.vector_db = vector_db

    async def create_note(self, note_in: NoteCreate, user_id: str) -> dict:
        # 1. Generate title from content
        title = await self.ai.generate_title_from_content(note_in.content)

        # 2. Insert note metadata into Supabase
        response = self.db.table("notes").insert({
            "user_id": user_id,
            "title": title,
            "content": note_in.content,
            "tags": note_in.tags
        }).execute()

        new_note = response.data[0]
        note_id = uuid.UUID(new_note['id'])

        # 3. Generate and store embedding (fire and forget is an option for speed)
        embedding = await self.ai.generate_embedding(note_in.content)
        await self.vector_db.upsert_note(note_id=note_id, user_id=user_id, vector=embedding)

        return new_note

    async def get_note_by_id(self, note_id: uuid.UUID, user_id: str) -> dict | None:
        # RLS in Supabase ensures the user_id check is redundant but good for clarity
        response = self.db.table("notes").select("*").eq("id", str(note_id)).eq("user_id", user_id).execute()
        return response.data[0] if response.data else None

    def get_all_notes(self, user_id: str, page: int, page_size: int) -> list[dict]:
        offset = (page - 1) * page_size
        response = self.db.table("notes").select("*").eq("user_id", user_id).order("created_at", desc=True).range(offset, offset + page_size - 1).execute()
        return response.data

    async def update_note(self, note_id: uuid.UUID, note_in: NoteUpdate, user_id: str) -> dict | None:
        # Check if the note exists and belongs to the user first
        existing_note = await self.get_note_by_id(note_id, user_id)
        if not existing_note:
            return None

        update_data = note_in.model_dump(exclude_unset=True)

        if not update_data:
            return existing_note # Nothing to update

        response = self.db.table("notes").update(update_data).eq("id", str(note_id)).execute()
        updated_note = response.data[0]

        # If content was updated, regenerate and upsert embedding
        if "content" in update_data:
            embedding = await self.ai.generate_embedding(updated_note['content'])
            await self.vector_db.upsert_note(note_id=note_id, user_id=user_id, vector=embedding)

        return updated_note

    async def delete_note(self, note_id: uuid.UUID, user_id: str) -> bool:
        # RLS handles security, this is just to confirm the operation
        response = self.db.table("notes").delete().eq("id", str(note_id)).eq("user_id", user_id).execute()

        if response.data:
            # Also delete from vector DB
            await self.vector_db.delete_note(note_id=note_id)
            return True
        return False

    async def search_user_notes(self, query: str, user_id: str) -> list[dict]:
        # 1. Generate embedding for the search query
        query_embedding = await self.ai.generate_embedding(query)

        # 2. Search in Qdrant for similar note IDs for this user
        note_ids = await self.vector_db.search_notes(user_id=user_id, query_vector=query_embedding)

        if not note_ids:
            return []

        # 3. Retrieve full note data from Supabase for the found IDs
        str_note_ids = [str(nid) for nid in note_ids]
        response = self.db.table("notes").select("*").in_("id", str_note_ids).execute()

        # Re-order results based on Qdrant's similarity ranking
        note_map = {note['id']: note for note in response.data}
        ordered_notes = [note_map[str(nid)] for nid in note_ids if str(nid) in note_map]

        return ordered_notes
