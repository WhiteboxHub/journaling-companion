import json
from pathlib import Path
from src.data_generation.clients.pew_client import get_pew_age_distribution
# Future: add more clients (census, statista, etc.)

def build_distribution_from_clients() -> dict:
    # Pull data from one or more public sources
    age_dist = get_pew_age_distribution()

    # Merge with other handcrafted or static fallback distributions
    distribution = {
        "age_group": age_dist,
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
    return distribution

def save_distribution(distribution: dict, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(distribution, f, indent=2)

if __name__ == "__main__":
    dist = build_distribution_from_clients()
    save_distribution(dist, Path("data/metadata/distribution.json"))
    print("[✓] Saved: data/metadata/distribution.json")