# evaluation_metrics.py

from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from detoxify import Detoxify
import torch
import numpy as np

# --- ROUGE/BERTScore: Summarization quality ---
def compute_rouge(pred: str, ref: str):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)
    return scorer.score(ref, pred)

def compute_bertscore(pred: str, ref: str):
    P, R, F1 = bert_score([pred], [ref], lang="en", model_type="bert-base-uncased", verbose=False)
    return {"precision": P[0].item(), "recall": R[0].item(), "f1": F1[0].item()}

# --- Empathy Score: Pretrained classifier (EmpathBERT-style) ---
def load_empathy_classifier():
    model_name = "mrm8488/bert-tiny-finetuned-emotion"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model.eval(), tokenizer

def compute_empathy_score(text: str, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1).numpy()[0]
    return float(np.max(probs))  # Max probability of any empathetic emotion

# --- Personalization: Cosine sim between prompt & journal embeddings ---
def compute_personalization(prompt: str, journal_history: List[str]):
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    prompt_emb = embedder.encode([prompt], convert_to_tensor=True)
    history_emb = embedder.encode(journal_history, convert_to_tensor=True)
    sim_scores = util.cos_sim(prompt_emb, history_emb)[0]
    return float(torch.max(sim_scores).item())  # Highest sim to any entry

# --- Safety: Detoxify score (toxicity probability) ---
def compute_safety_score(text: str):
    detox = Detoxify("original")
    results = detox.predict(text)
    return {"toxicity": results["toxicity"]}

# --- Example use ---
if __name__ == "__main__":
    pred_summary = "You've had a stressful week but found peace in moments of connection."
    ref_summary = "This week was difficult, but you were able to find relief through small acts of self-care and support."

    prompt = "How are you taking care of yourself today?"
    journal_history = ["I feel anxious about work.", "Took a long walk to clear my head.", "I talked to my friend finally."]

    print("\n[ROUGE]")
    print(compute_rouge(pred_summary, ref_summary))

    print("\n[BERTScore]")
    print(compute_bertscore(pred_summary, ref_summary))

    print("\n[Empathy Score]")
    model, tokenizer = load_empathy_classifier()
    print(compute_empathy_score(pred_summary, model, tokenizer))

    print("\n[Personalization Score]")
    print(compute_personalization(prompt, journal_history))

    print("\n[Safety Score]")
    print(compute_safety_score(prompt))