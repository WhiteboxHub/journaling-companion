import json
import random
from pathlib import Path
from typing import Dict, List

# --- Step 1: Try loading an existing distribution.json ---
def load_distribution(distribution_path: str) -> Dict:
    try:
        with open(distribution_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[Warning] Distribution file not found at {distribution_path}. Using fallback sample.")
        return get_sample_distribution()

# --- Step 2: Sample fallback distribution if no public data fetched ---
def get_sample_distribution() -> Dict:
    return {
        "age_group": {
            "18-24": 0.2,
            "25-34": 0.3,
            "35-44": 0.2,
            "45-54": 0.2,
            "55+": 0.1
        },
        "gender": {
            "male": 0.45,
            "female": 0.45,
            "non_binary": 0.05,
            "prefer_not_to_say": 0.05
        },
        "occupation": {
            "student": 0.2,
            "engineer": 0.2,
            "teacher": 0.15,
            "artist": 0.15,
            "therapist": 0.1,
            "retired": 0.2
        },
        "writing_style": {
            "reflective": 0.3,
            "expressive": 0.3,
            "concise": 0.2,
            "analytical": 0.2
        },
        "personality": {
            "optimistic": 0.25,
            "anxious": 0.25,
            "creative": 0.25,
            "reserved": 0.25
        },
        "journaling_frequency": {
            "daily": 0.4,
            "weekly": 0.4,
            "irregular": 0.2
        }
    }

# --- Step 3: Sampling helper ---
def weighted_sample(options: Dict[str, float]) -> str:
    items, weights = zip(*options.items())
    return random.choices(items, weights=weights, k=1)[0]

# --- Step 4: Generate synthetic personas ---
def generate_personas(distribution: Dict, n: int = 10) -> List[Dict]:
    personas = []
    for i in range(n):
        persona = {
            "user_id": f"user_{i+1:02d}"
        }
        for attr, options in distribution.items():
            persona[attr] = weighted_sample(options)
        personas.append(persona)
    return personas

# --- Step 5: Save outputs ---
def save_json(data, path: Path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

# --- Entry Point ---
if __name__ == "__main__":
    output_dir = Path("data/metadata")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load or generate fallback distribution
    distribution = load_distribution("data/metadata/distribution.json")
    save_json(distribution, output_dir / "distribution.json")

    # Generate and save personas
    personas = generate_personas(distribution, n=10)
    save_json(personas, output_dir / "personas.json")

    print("[✓] Saved: distribution.json and personas.json")
