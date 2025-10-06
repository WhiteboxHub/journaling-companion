# generate_prompt_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.rag.retrieve_user_history import retrieve_similar_entries
from src.rag.generate_prompt import generate_prompt_from_entries

app = FastAPI(title="Journaling Companion: Prompt Generator")

# --- Request/Response Models ---
class PromptRequest(BaseModel):
    user_id: str
    query_text: str
    top_k: Optional[int] = 3

class PromptResponse(BaseModel):
    past_entries: list[str]
    prompt: str

# --- API Route ---
@app.post("/generate_prompt", response_model=PromptResponse)
def generate_prompt_endpoint(request: PromptRequest):
    try:
        entries = retrieve_similar_entries(
            query_text=request.query_text,
            user_id=request.user_id,
            top_k=request.top_k
        )
        if not entries:
            raise HTTPException(status_code=404, detail="No relevant entries found for user.")

        prompt = generate_prompt_from_entries(entries)
        return {"past_entries": entries, "prompt": prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
