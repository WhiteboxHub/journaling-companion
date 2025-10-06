import json
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# --- Config ---
DATA_PATH = Path("data/interim/journals.jsonl")
MODEL_PATH = Path("models/emotion_classifier")
LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
    "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear",
    "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral"
]

# --- Load entries ---
def load_entries(path):
    entries = []
    with open(path, 'r') as f:
        for line in f:
            try:
                row = json.loads(line)
                assert "entry" in row and "emotions" in row
                entries.append(row)
            except Exception as e:
                print(f"[!] Skipped bad row: {e}")
    return entries

# --- Visualize label distribution ---
def plot_emotion_distribution(entries):
    all_emotions = [emo for e in entries for emo in e["emotions"]]
    counts = Counter(all_emotions)
    plt.figure(figsize=(14, 6))
    plt.bar(counts.keys(), counts.values(), color='skyblue')
    plt.title("Emotion Label Distribution in Journal Dataset")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/emotion_label_distribution.png")
    print("[✓] Saved: emotion_label_distribution.png")

# --- Load model and tokenizer ---
def load_model():
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    return model, tokenizer

# --- Predict on unseen data ---
def predict_emotions(model, tokenizer, texts, top_k=3):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).numpy()
    predictions = []
    for p in probs:
        top_labels = [LABELS[i] for i in np.argsort(p)[::-1][:top_k] if p[i] > 0.5]
        predictions.append(top_labels)
    return predictions

# --- Main ---
def main():
    entries = load_entries(DATA_PATH)
    print(f"[✓] Loaded {len(entries)} valid entries")

    # 1. Visualize label distribution
    plot_emotion_distribution(entries)

    # 2. Load model and predict on 5 samples
    model, tokenizer = load_model()
    test_samples = [e['entry'] for e in entries[:5]]
    true_labels = [e['emotions'] for e in entries[:5]]
    pred_labels = predict_emotions(model, tokenizer, test_samples)

    for i, (text, true, pred) in enumerate(zip(test_samples, true_labels, pred_labels)):
        print(f"\n--- Sample {i+1} ---")
        print(f"Text: {text}\nTrue: {true}\nPred: {pred}")

if __name__ == "__main__":
    Path("outputs").mkdir(exist_ok=True)
    main()