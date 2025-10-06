from fastapi import FastAPI
from src.api.journal_routes import router as journal_router

app = FastAPI(title="Journaling Companion API")
app.include_router(journal_router)