# reframing_generator.py

from openai import OpenAI
from typing import List

# --- Initialize OpenAI ---
client = OpenAI()

# --- Prompt Template with Safety Guardrails ---
REFRAME_PROMPT_TEMPLATE = """
You are an empathetic assistant helping users reframe negative or difficult experiences.

Input journal entry:
"""
{entry}
"""

Extract the main concern, and then generate a gentle, encouraging reframe.
Use this structure:

"It sounds like {extracted concern}. Remember that {encouragement}. Tomorrow is a new opportunity."
"""

# --- Generate reframe using GPT-4 ---
def generate_reframe(entry_text: str) -> str:
    prompt = REFRAME_PROMPT_TEMPLATE.format(entry=entry_text)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

# --- Example usage ---
if __name__ == "__main__":
    sample_entry = (
        "I totally messed up the presentation. I stumbled over my words and forgot key points."
        " I feel embarrassed and like I let my team down."
    )

    reframe = generate_reframe(sample_entry)
    print("\n--- Reframed Output ---")
    print(reframe)