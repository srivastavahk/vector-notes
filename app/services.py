from app.database import Database
from app.vector_db import VectorDB
from app.embeddings import EmbeddingService
from app.models import Note, NoteCreate, NoteUpdate

db = Database()
vector_db = VectorDB()
embedding_service = EmbeddingService()

class NoteService:
    @staticmethod
    def create_note(user_id: str, note: NoteCreate) -> Note:
        created_note = db.create_note(user_id, note)
        vector = embedding_service.generate_embedding(f"{note.title} {note.content}")
        vector_db.upsert_vector(
            note_id=created_note['id'],
            user_id=user_id,
            vector=vector,
            payload={
                "title": note.title,
                "content": note.content,
                "tags": note.tags or []
            }
        )
        return created_note

    @staticmethod
    def update_note(note_id: str, user_id: str, update_data: NoteUpdate) -> Note:
        note = db.get_note(note_id, user_id)
        if not note:
            return None

        updated_note = db.update_note(note_id, user_id, update_data)
        if not updated_note:
            return None

        # Update vector if content changed
        if update_data.content or update_data.title:
            new_content = update_data.content or note['content']
            new_title = update_data.title or note['title']
            vector = embedding_service.generate_embedding(f"{new_title} {new_content}")

            payload = {
                "title": new_title,
                "content": new_content,
                "tags": update_data.tags or note['tags'] or []
            }
            vector_db.upsert_vector(note_id, user_id, vector, payload)

        return updated_note

    @staticmethod
    def delete_note(note_id: str, user_id: str):
        db.delete_note(note_id, user_id)
        vector_db.delete_vector(note_id)

    @staticmethod
    def get_note(note_id: str, user_id: str) -> Note:
        return db.get_note(note_id, user_id)

    @staticmethod
    def list_notes(user_id: str) -> list[Note]:
        return db.list_notes(user_id)

class SearchService:
    @staticmethod
    def semantic_search(user_id: str, query: str, limit: int = 5) -> list:
        vector = embedding_service.generate_embedding(query)
        results = vector_db.search_similar(user_id, vector, limit)
        return results
