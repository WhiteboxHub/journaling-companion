# emotion_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# --- Load model and tokenizer ---
MODEL_PATH = "models/emotion_classifier"
LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
    "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear",
    "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral"
]

app = FastAPI(title="Emotion Classifier API", description="Predict emotions from journal text")

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model.eval()

# --- Request/Response Schema ---
class EmotionRequest(BaseModel):
    text: str
    threshold: float = 0.5

class EmotionResponse(BaseModel):
    emotions: list[str]

# --- Prediction logic ---
def predict_emotions(text: str, threshold: float = 0.5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).numpy()[0]
    predicted = [LABELS[i] for i, p in enumerate(probs) if p >= threshold]
    return predicted

# --- API Route ---
@app.post("/predict_emotions", response_model=EmotionResponse)
def predict(request: EmotionRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text input is required")
    emotions = predict_emotions(request.text, request.threshold)
    return {"emotions": emotions}