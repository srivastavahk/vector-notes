from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client
from app.core.config import settings
from supabase_auth.errors import AuthApiError

# Supabase client setup
supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Not used directly, just for docs

async def get_current_user(request: Request):
    """Dependency to get and validate the current user from Supabase JWT."""
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    token = token.replace("Bearer ", "")

    try:
        user_response = supabase_client.auth.get_user(token)
        return user_response.user
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {e.message}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def get_supabase_client() -> Client:
    return supabase_client
