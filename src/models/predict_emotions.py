# predict_emotions.py

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

# --- Config ---
MODEL_PATH = "models/emotion_classifier"
LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
    "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear",
    "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral"
]

# --- Load model ---
def load_model():
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model.eval()
    return model, tokenizer

# --- Predict ---
def predict_emotions(text, model, tokenizer, threshold=0.5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).numpy()[0]
    predicted_labels = [LABELS[i] for i, p in enumerate(probs) if p >= threshold]
    return predicted_labels

# --- CLI Entry Point ---
def main():
    parser = argparse.ArgumentParser(description="Emotion Tagging for Journal Text")
    parser.add_argument("--text", type=str, required=True, help="Journal entry text")
    parser.add_argument("--threshold", type=float, default=0.5, help="Prediction threshold")
    args = parser.parse_args()

    model, tokenizer = load_model()
    emotions = predict_emotions(args.text, model, tokenizer, args.threshold)

    print("\nJournal Entry:")
    print(args.text)
    print("\nPredicted Emotions:")
    print(emotions if emotions else "[No emotion above threshold]")

if __name__ == "__main__":
    main()
    