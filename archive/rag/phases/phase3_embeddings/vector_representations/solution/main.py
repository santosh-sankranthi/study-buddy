"""SOLUTION -- Vector Representations Invariants."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import DEMO_VECS, cosine_similarity, rank_by_similarity

def verify_invariants() -> dict[str, float]:
    return {
        "identity": round(cosine_similarity([3.0, 4.0], [3.0, 4.0]), 4),
        "orthogonal": round(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 4),
        "opposite": round(cosine_similarity([1.0, 0.0], [-1.0, 0.0]), 4),
    }

def rank_physics_query() -> list[tuple[str, float]]:
    return rank_by_similarity([0.05, 0.95, 0.05], DEMO_VECS)

OBSERVATION = "Cosine similarity cleanly separates orthogonal scientific domains even with shared vocabulary."

if __name__ == "__main__":
    print(verify_invariants())
