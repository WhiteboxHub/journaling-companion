import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from openai import OpenAI

# --- Config ---
NUM_ENTRIES = 600
OUTPUT_PATH = Path("data/interim/journals.jsonl")
PERSONA_PATH = Path("data/metadata/personas.json")

# Initialize OpenAI API client (ensure your key is set in environment or securely loaded)
client = OpenAI()

# --- Load personas ---
def load_personas(path: Path) -> List[Dict]:
    with open(path, 'r') as f:
        return json.load(f)

# --- Generate a journal entry using GPT ---
def generate_entry(persona: Dict) -> Dict:
    user_id = persona['user_id']
    prompt = f"""
    You are a journaling assistant helping a {persona['age_group']} {persona['gender']} who works as a {persona['occupation']}.
    They are {persona['personality']} and write in a {persona['writing_style']} style.

    Generate a realistic, reflective journal entry for today. Focus on themes like stress, joy, reflection, or daily experiences.
    Include a short entry (~100-150 words). Then, annotate with:
      - emotions (e.g., sadness, happiness, anxiety)
      - topic (e.g., work, relationships, self-growth)
      - tone (positive, neutral, negative)
      - a supportive summary of their entry
      - a positively framed reframe or encouragement
      - a gentle, empathetic follow-up question

    Format the output as a JSON object with keys: 'entry', 'emotions', 'topic', 'tone', 'summary', 'reframe', 'prompt'.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    try:
        generated = json.loads(response.choices[0].message.content)
    except Exception as e:
        print("[!] Failed to parse GPT output:", e)
        return None

    return {
        "user_id": user_id,
        "date": datetime.now().strftime('%Y-%m-%d'),
        **generated
    }

# --- Main orchestration ---
def main():
    personas = load_personas(PERSONA_PATH)
    entries = []

    for i in range(NUM_ENTRIES):
        persona = random.choice(personas)
        print(f"Generating entry {i+1}/{NUM_ENTRIES} for {persona['user_id']}")
        entry = generate_entry(persona)
        if entry:
            entries.append(entry)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")

    print(f"[✓] Saved {len(entries)} entries to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
