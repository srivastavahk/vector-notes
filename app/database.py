from supabase import create_client
from app.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)

class Database:
    def __init__(self):
        self.client = supabase

    def get_user_by_email(self, email: str):
        response = self.client.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None

    def create_user(self, email: str):
        response = self.client.table('users').insert({'email': email}).execute()
        return response.data[0]

    def create_note(self, user_id: str, note: NoteCreate):
        note_data = note.dict()
        note_data['user_id'] = user_id
        response = self.client.table('notes').insert(note_data).execute()
        return response.data[0]

    def get_note(self, note_id: str, user_id: str):
        response = self.client.table('notes').select('*').eq('id', note_id).eq('user_id', user_id).execute()
        return response.data[0] if response.data else None

    def update_note(self, note_id: str, user_id: str, update_data: NoteUpdate):
        update_data = {k: v for k, v in update_data.dict().items() if v is not None}
        if not update_data:
            return None

        response = self.client.table('notes').update(update_data).eq('id', note_id).eq('user_id', user_id).execute()
        return response.data[0] if response.data else None

    def delete_note(self, note_id: str, user_id: str):
        self.client.table('notes').delete().eq('id', note_id).eq('user_id', user_id).execute()

    def list_notes(self, user_id: str):
        response = self.client.table('notes').select('*').eq('user_id', user_id).execute()
        return response.data
