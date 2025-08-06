from fastapi import FastAPI
from app.api.routes import api_router
from app.core.middleware import add_middlewares

app = FastAPI(title="AudioScribe")
add_middlewares(app)
app.include_router(api_router)
