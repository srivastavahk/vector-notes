## Architecture Overview

The Python/FastAPI implementation follows the same clean architecture principles:

1. **Controllers**: FastAPI routers handle HTTP requests
2. **Services**: Business logic layer
3. **Repositories**: Database and vector store operations
4. **Models**: Pydantic schemas for data validation
5. **Dependencies**: Authentication and other reusable components

### Key Components

- **Authentication**: JWT token verification with PyJWT
- **Note Management**: CRUD operations via Supabase PostgreSQL
- **Embeddings**: OpenAI's text-embedding-ada-002 model
- **Vector Search**: Qdrant Cloud for similarity search

### Environment Variables

| Variable          | Description                     |
|-------------------|---------------------------------|
| SUPABASE_URL      | Supabase project URL            |
| SUPABASE_KEY      | Supabase API key                |
| OPENAI_API_KEY    | OpenAI API key                  |
| QDRANT_URL        | Qdrant cluster URL              |
| QDRANT_API_KEY    | Qdrant API key                  |
| JWT_SECRET        | Secret for JWT token signing    |
| EMBEDDING_MODEL   | OpenAI embedding model          |

### API Endpoints

**Authentication**
- Obtain JWT from Supabase Auth
- Include in header: `Authorization: Bearer <token>`

**Notes API**
- `POST /api/notes` - Create note
- `GET /api/notes` - List user's notes
- `GET /api/notes/{id}` - Get single note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note

**Search API**
- `GET /api/search?query=<text>&limit=5` - Semantic search

### Python Stack Advantages

1. **FastAPI**:
   - Automatic OpenAPI documentation
   - Async support for I/O bound operations
   - Built-in data validation with Pydantic
   - Dependency injection system

2. **Supabase Python Client**:
   - Direct access to PostgreSQL database
   - Simplified authentication flows

3. **Qdrant Client**:
   - Native support for vector operations
   - Efficient similarity search

4. **Pydantic**:
   - Runtime data validation
   - Automatic API documentation generation
   - Settings management

### Future Extensibility

1. **RAG Integration**:
   ```python
   @router.post("/ask")
   async def ask_question(question: str, current_user: User = Depends(get_current_user)):
       # 1. Perform semantic search
       # 2. Feed context to LLM
       # 3. Return generated response
