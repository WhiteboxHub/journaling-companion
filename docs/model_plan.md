## Model Plan – Journaling Companion

### Problem Statement
Build a private, empathetic, intelligent journaling assistant that:
- Encourages daily reflection via personalized prompts
- Offers emotionally aware reframing of negative experiences
- Summarizes weekly themes and emotional trends

### Tasks & Model Types

| Task                        | Type                     | Method / Model                         |
|-----------------------------|--------------------------|----------------------------------------|
| Prompt Generation           | Conditional Generation   | GPT-4 + Sentence-BERT (RAG)            |
| Reframing Generator         | Tone-controlled Generation | GPT-4 with structured template       |
| Weekly Summarization        | Multi-doc Summarization  | Sentence-BERT + GPT-4 (clustered)      |
| Emotion Classification      | Multi-label Classification | DistilRoBERTa (GoEmotions fine-tuned) |

### Model Components

- **Sentence Embedding Model**: `all-MiniLM-L6-v2` (RAG + clustering)
- **Prompt Generator**: GPT-4 with few-shot examples
- **Reframe Generator**: GPT-4, template-constrained
- **Summarizer**: Sentence clustering + GPT-4
- **Emotion Classifier**: fine-tuned `distilroberta-base` on GoEmotions

### Data Flow
1. User journals via UI → stored in MongoDB
2. API retrieves recent entries → generates new prompt
3. User writes → classifier tags emotion → reframing generated
4. Weekly background task clusters and summarizes data

### Safety Guardrails
- Template structure for reframes
- Toxicity check (Detoxify)
- Empathy check via classifier

---

## ✅ Models Used

| Model                                | Usage                        |
|-------------------------------------|------------------------------|
| `openai/gpt-4`                       | Prompt, Summary, Reframe     |
| `sentence-transformers/all-MiniLM-L6-v2` | RAG, clustering, personalization |
| `distilroberta-goemotion` (custom)  | Emotion tagging              |
| `unitary/toxic-bert` or Detoxify    | Safety filter (toxicity)     |

---

## 🧪 Evaluation Metrics

| Metric           | Description                                |
|------------------|--------------------------------------------|
| ROUGE, BERTScore | Summary quality vs ground-truth            |
| Empathy Score    | Max probability from empathy classifier    |
| Personalization  | Cosine similarity between prompt + history |
| Toxicity Score   | Detoxify: probability of harmful language  |