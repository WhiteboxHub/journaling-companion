from sentence_transformers import SentenceTransformer
import faiss
import json
from pathlib import Path
from tqdm import tqdm
import numpy as np
import pickle

# --- Config ---
DATA_PATH = Path("data/interim/journals.jsonl")
INDEX_DIR = Path("data/processed/faiss_index")
EMBED_MODEL = "all-MiniLM-L6-v2"

# --- Load journal entries ---
def load_journal_entries(path):
    entries = []
    with open(path, 'r') as f:
        for line in f:
            row = json.loads(line)
            if "entry" in row and "user_id" in row:
                entries.append(row)
    return entries

# --- Embed all entries ---
def embed_entries(model, entries):
    texts = [e["entry"] for e in entries]
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
    return embeddings

# --- Build FAISS index ---
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

# --- Save index + metadata ---
def save_index(index, entries):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_DIR / "journal_index.faiss"))
    with open(INDEX_DIR / "journal_metadata.pkl", "wb") as f:
        pickle.dump(entries, f)

# --- Main ---
def main():
    print("[+] Loading journal entries...")
    entries = load_journal_entries(DATA_PATH)

    print(f"[+] Loaded {len(entries)} entries. Embedding...")
    model = SentenceTransformer(EMBED_MODEL)
    embeddings = embed_entries(model, entries)

    print("[+] Building FAISS index...")
    index = build_faiss_index(np.array(embeddings))

    print("[+] Saving index and metadata...")
    save_index(index, entries)

    print("[✓] FAISS index built and saved to data/processed/faiss_index/")

if __name__ == "__main__":
    main()
