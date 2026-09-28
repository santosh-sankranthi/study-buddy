"""EXERCISE -- Vector Geometry & Adversarial Sentences.

The demo ranked biological statements using 3-D toy vectors.
Your twist: verify mathematical invariants (identity=1.0, orthogonal=0.0, opposite=-1.0),
then observe how an adversarial phrasing behaves under cosine similarity.

Run when done:
    python phases/phase3_embeddings/vector_representations/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import DEMO_VECS, cosine_similarity, rank_by_similarity

# TODO(1): Implement verify_invariants() -> dict[str, float]
#   - identity: cosine_similarity([3.0, 4.0], [3.0, 4.0]) -> 1.0
#   - orthogonal: cosine_similarity([1.0, 0.0], [0.0, 1.0]) -> 0.0
#   - opposite: cosine_similarity([1.0, 0.0], [-1.0, 0.0]) -> -1.0
def verify_invariants() -> dict[str, float]:
    raise NotImplementedError("TODO(1): implement verify_invariants")


# TODO(2): Write one sentence describing what cosine similarity measures:
OBSERVATION = ""


if __name__ == "__main__":
    print("Invariants:", verify_invariants())
    print("Observation:", OBSERVATION)
