import json
from pathlib import Path
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import numpy as np
import torch

# --- Config ---
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"
DATA_PATH = Path("data/interim/journals.jsonl")
OUTPUT_DIR = Path("models/emotion_classifier")
LABELS = [  # Based on GoEmotions
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
    "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear",
    "gratitude", "grief", "joy", "love", "nervousness", "optimism", "pride", "realization",
    "relief", "remorse", "sadness", "surprise", "neutral"
]

# --- Load and prepare dataset ---
def load_data(path: Path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            row = json.loads(line)
            data.append({
                "text": row["entry"],
                "labels": row.get("emotions", [])
            })
    return data

def binarize_labels(data):
    mlb = MultiLabelBinarizer(classes=LABELS)
    Y = mlb.fit_transform([d["labels"] for d in data])
    return Y, mlb

# --- Tokenization ---
def tokenize_function(examples, tokenizer):
    return tokenizer(examples["text"], truncation=True, padding=True)

# --- Compute metrics ---
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    probs = torch.sigmoid(torch.tensor(logits)).numpy()
    preds = (probs >= 0.5).astype(int)
    acc = (preds == labels).mean()
    return {"accuracy": acc}

# --- Main ---
def main():
    raw_data = load_data(DATA_PATH)
    Y, mlb = binarize_labels(raw_data)

    texts = [d["text"] for d in raw_data]
    data = Dataset.from_dict({"text": texts, "labels": Y.tolist()})

    train_test = data.train_test_split(test_size=0.2)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenized = train_test.map(lambda x: tokenize_function(x, tokenizer), batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        problem_type="multi_label_classification"
    )

    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=4,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()
    trainer.save_model(str(OUTPUT_DIR))
    print(f"[✓] Saved fine-tuned model to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
