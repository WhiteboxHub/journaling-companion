from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from src.utils.mongo_utils import journal_entries

router = APIRouter()

# --- Models ---
class JournalEntry(BaseModel):
    user_id: str
    date: str  # Format YYYY-MM-DD
    entry: str
    emotions: Optional[List[str]] = []
    tone: Optional[str] = None
    prompt: Optional[str] = None
    reframe: Optional[str] = None
    summary: Optional[str] = None

# --- POST /submit_entry ---
@router.post("/submit_entry")
def submit_entry(entry: JournalEntry):
    doc = entry.dict()
    doc["timestamp"] = datetime.utcnow()
    result = journal_entries.insert_one(doc)
    return {"status": "success", "id": str(result.inserted_id)}

# --- GET /get_entries ---
@router.get("/get_entries", response_model=List[JournalEntry])
def get_entries(user_id: str, days: int = 7):
    cutoff = datetime.utcnow() - timedelta(days=days)
    results = journal_entries.find({"user_id": user_id, "timestamp": {"$gte": cutoff}})
    return [JournalEntry(**{k: v for k, v in r.items() if k in JournalEntry.__fields__}) for r in results]

# --- GET /get_summary ---
@router.get("/get_summary")
def get_summary(user_id: str):
    doc = journal_entries.find_one(
        {"user_id": user_id, "summary": {"$exists": True}},
        sort=[("timestamp", -1)]
    )
    if not doc:
        raise HTTPException(status_code=404, detail="No summary found.")
    return {
        "date": doc["date"],
        "summary": doc["summary"],
        "emotions": doc.get("emotions", [])
    }
