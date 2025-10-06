## Data Schema – Journaling Companion

### Collection: `journal_entries`

Stores all user journal data and associated metadata.

```json
{
  "user_id": "user_01",
  "date": "2025-10-05",
  "entry": "Today was rough. I felt anxious during my meeting.",
  "emotions": ["anxiety", "insecurity"],
  "tone": "negative",
  "prompt": "What triggered those feelings today?",
  "reframe": "It sounds like that meeting triggered some anxiety. Remember that showing up is a win. Tomorrow is a new opportunity.",
  "summary": null,
  "timestamp": "2025-10-05T22:15:00Z"
}
```

---

### Collection: `users` (optional, for future auth)

```json
{
  "user_id": "user_01",
  "name": "Alex",
  "persona": {
    "age_group": "25-34",
    "occupation": "engineer",
    "writing_style": "reflective",
    "personality": "anxious"
  },
  "created_at": "2025-10-01T00:00:00Z"
}
```

---

### Derived Data

#### Weekly Summary (generated via `/generate_summary`):
```json
{
  "user_id": "user_01",
  "date": "2025-10-07",
  "summary": "You’ve been reflecting on difficult work moments, but also reached out to a friend which helped you cope.",
  "emotion_trends": {
    "anxiety": 3,
    "relief": 2,
    "gratitude": 1
  }
}
```

---

### Embeddings (optional for FAISS or vector DB)
```json
{
  "user_id": "user_01",
  "entry_id": "...",
  "embedding": [0.1, 0.02, -0.5, ...],
  "source": "entry",
  "timestamp": "2025-10-05T22:15:00Z"
}
```

> Note: Embeddings stored separately in memory (FAISS), not persisted in Mongo unless needed for audit/debugging.

---

### Fields Used for Evaluation

| Field       | Used For                    |
|-------------|-----------------------------|
| `entry`     | Prompting, summarization    |
| `prompt`    | Personalization analysis     |
| `emotions`  | Trend chart, classifier eval |
| `reframe`   | Empathy/toxicity evaluation  |
| `summary`   | BERTScore, ROUGE eval       |
