# evaluate_reframes.py

import json
import csv
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from src.evaluation.evaluation_metrics import (
    compute_empathy_score,
    compute_safety_score
)
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# --- Config ---
JOURNAL_PATH = Path("data/interim/journals.jsonl")
RESULTS_PATH = Path("outputs/reframe_eval_results.csv")
MODEL_NAME = "gpt-4"
N_SAMPLES = 100

client = OpenAI()

# Load empathy model once
empathy_model, empathy_tokenizer = AutoModelForSequenceClassification.from_pretrained(
    "mrm8488/bert-tiny-finetuned-emotion"
), AutoTokenizer.from_pretrained("mrm8488/bert-tiny-finetuned-emotion")
empathy_model.eval()

# Template
REFRAME_TEMPLATE = """
You are an empathetic assistant helping users reframe difficult experiences.

Input journal entry:
"""
{entry}
"""

Respond with a message like:
"It sounds like {{concern}}. Remember that {{encouragement}}. Tomorrow is a new opportunity."
"""

# Generate from GPT

def generate_reframe(entry: str, model_name="gpt-4") -> str:
    prompt = REFRAME_TEMPLATE.format(entry=entry)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# --- Load samples ---
def load_negative_entries(path, limit=100):
    samples = []
    with open(path, 'r') as f:
        for line in f:
            row = json.loads(line)
            if row.get("tone") == "negative":
                samples.append(row)
            if len(samples) >= limit:
                break
    return samples

# --- Evaluate and save ---
def evaluate_reframes(samples, model_name="gpt-4"):
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "entry", "reframe", "empathy", "toxicity", "model", "date"])

        for sample in samples:
            entry = sample["entry"]
            user_id = sample["user_id"]

            try:
                reframe = generate_reframe(entry, model_name)
                empathy = compute_empathy_score(reframe, empathy_model, empathy_tokenizer)
                toxicity = compute_safety_score(reframe)["toxicity"]

                writer.writerow([
                    user_id, entry, reframe, f"{empathy:.4f}", f"{toxicity:.4f}", model_name, datetime.utcnow().isoformat()
                ])
                print(f"[✓] {user_id}: empathy={empathy:.2f}, toxicity={toxicity:.2f}")

            except Exception as e:
                print(f"[!] Error on entry: {e}")

# --- Main ---
if __name__ == "__main__":
    print("[+] Loading samples...")
    samples = load_negative_entries(JOURNAL_PATH, limit=N_SAMPLES)
    evaluate_reframes(samples, model_name=MODEL_NAME)