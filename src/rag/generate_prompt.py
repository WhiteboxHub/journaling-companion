# generate_prompt.py

from openai import OpenAI
from typing import List
import os

# --- Config ---
MODEL_NAME = "gpt-4"
MAX_ENTRIES = 3

# Initialize OpenAI client
client = OpenAI()

# --- Prompt template ---
PROMPT_TEMPLATE = """
You are an empathetic journaling assistant. Based on the user's past journal entries, generate a thoughtful and supportive journaling prompt that encourages reflection.

Past Entries:
{context_entries}

Now, write a gentle follow-up prompt that acknowledges their experiences and encourages them to write today.
"""

# --- Format context into prompt ---
def format_context(entries: List[str]) -> str:
    return "\n".join([f"{i+1}. {e}" for i, e in enumerate(entries[:MAX_ENTRIES])])

# --- Generate prompt ---
def generate_prompt_from_entries(entries: List[str]) -> str:
    context_text = format_context(entries)
    final_prompt = PROMPT_TEMPLATE.format(context_entries=context_text)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

# --- Example usage ---
if __name__ == "__main__":
    sample_entries = [
        "I felt anxious about work and couldn’t sleep well.",
        "My team meeting went poorly — I couldn’t speak up.",
        "Tried to take a walk to clear my head, but it didn’t help much."
    ]

    prompt = generate_prompt_from_entries(sample_entries)
    print("\n--- Generated Prompt ---")
    print(prompt)