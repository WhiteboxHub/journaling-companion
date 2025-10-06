# generate_summary_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime, timedelta
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans
import numpy as np

# --- Load journal entries (mock database) ---
JOURNAL_PATH = "data/interim/journals.jsonl"

# --- Model setup ---
client = OpenAI()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI(title="Journaling Companion: Weekly Summary Generator")

# --- Request and Response Schemas ---
class SummaryRequest(BaseModel):
    user_id: str
    days: Optional[int] = 7
    clusters: Optional[int] = 3

class SummaryResponse(BaseModel):
    summary: str
    emotion_trends: dict
    entries_used: List[str]

# --- Helper: Load user journal entries ---
def load_user_entries(user_id: str, days: int) -> List[dict]:
    entries = []
    cutoff = datetime.now() - timedelta(days=days)
    with open(JOURNAL_PATH, 'r') as f:
        for line in f:
            row = json.loads(line)
            if row.get("user_id") != user_id:
                continue
            try:
                entry_date = datetime.strptime(row["date"], "%Y-%m-%d")
                if entry_date >= cutoff:
                    entries.append(row)
            except:
                continue
    return entries

# --- Helper: Cluster entries by topic using embeddings ---
def cluster_entries(entries: List[str], n_clusters: int) -> List[List[str]]:
    if len(entries) <= n_clusters:
        return [[e] for e in entries]
    embeddings = embedding_model.encode(entries)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    clustered = [[] for _ in range(n_clusters)]
    for i, label in enumerate(labels):
        clustered[label].append(entries[i])
    return clustered

# --- Helper: Summarize with GPT-4 ---
def summarize_clusters(clusters: List[List[str]]) -> str:
    summaries = []
    for cluster in clusters:
        joined = "\n".join(cluster)
        prompt = f"""
        The following journal entries are related:

        {joined}

        Write a short and supportive summary of the key themes.
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        summaries.append(response.choices[0].message.content.strip())
    return "\n\n".join(summaries)

# --- Helper: Extract emotion trends ---
def extract_emotion_trends(entries: List[dict]) -> dict:
    from collections import Counter
    trends = Counter()
    for e in entries:
        for emo in e.get("emotions", []):
            trends[emo] += 1
    return dict(trends.most_common(5))

# --- Route: POST /generate_summary ---
@app.post("/generate_summary", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    entries = load_user_entries(request.user_id, request.days)
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found for user in date range.")

    entry_texts = [e["entry"] for e in entries]
    clusters = cluster_entries(entry_texts, request.clusters)
    summary = summarize_clusters(clusters)
    emotion_summary = extract_emotion_trends(entries)

    return SummaryResponse(
        summary=summary,
        emotion_trends=emotion_summary,
        entries_used=entry_texts
    )