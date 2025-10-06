# retrieve_user_history.py

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from pathlib import Path

# --- Config ---
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = Path("data/processed/faiss_index/journal_index.faiss")
METADATA_PATH = Path("data/processed/faiss_index/journal_metadata.pkl")
TOP_K = 3

# --- Load index and metadata ---
def load_index_and_metadata():
    index = faiss.read_index(str(INDEX_PATH))
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

# --- Embed query using SBERT ---
def embed_query(text: str, model) -> np.ndarray:
    return model.encode([text])

# --- Retrieve top-N similar entries for a user (optionally filtered by user_id) ---
def retrieve_similar_entries(query_text: str, user_id: str = None, top_k: int = TOP_K) -> List[str]:
    model = SentenceTransformer(MODEL_NAME)
    index, metadata = load_index_and_metadata()

    query_embedding = embed_query(query_text, model)
    distances, indices = index.search(query_embedding, top_k * 2)  # retrieve more, filter later

    retrieved = []
    for idx in indices[0]:
        if idx >= len(metadata):
            continue
        row = metadata[idx]
        if user_id is None or row.get("user_id") == user_id:
            retrieved.append(row["entry"])
        if len(retrieved) == top_k:
            break

    return retrieved

# --- Example usage ---
if __name__ == "__main__":
    query = "I’ve been feeling stressed about work and not sleeping well."
    user_id = "user_01"
    history = retrieve_similar_entries(query_text=query, user_id=user_id, top_k=3)
    print("\n--- Retrieved Entries ---")
    for i, entry in enumerate(history):
        print(f"[{i+1}] {entry}\n")
