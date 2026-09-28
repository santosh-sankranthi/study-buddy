"""EXERCISE -- Vector Geometry & Cosine Similarity Invariants.

The demo ranked biological statements using 3-D toy vectors.
Your twist: verify the mathematical invariants of cosine_similarity(),
then rank candidates against a Physics query [0.05, 0.95, 0.05] and observe
whether Newton's laws dominate over biology statements.

Fill in every TODO. Run when done:
    python phases/phase3_embeddings/vector_math/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import DEMO_VECS, cosine_similarity, rank_by_similarity


# ── TODO(1): Verify mathematical invariants ──────────────────────────────────
def verify_invariants() -> dict[str, float]:
    """Test identity, orthogonality, and opposite directions."""
    # TODO(1a): identity: cosine_similarity([3.0, 4.0], [3.0, 4.0]) -> should be 1.0
    sim_identity = cosine_similarity([3.0, 4.0], [3.0, 4.0])
    # TODO(1b): orthogonal: cosine_similarity([1.0, 0.0], [0.0, 1.0]) -> should be 0.0
    sim_orthogonal = cosine_similarity([1.0, 0.0], [0.0, 1.0])
    # TODO(1c): opposite: cosine_similarity([1.0, 0.0], [-1.0, 0.0]) -> should be -1.0
    sim_opposite = cosine_similarity([1.0, 0.0], [-1.0, 0.0])

    return {
        "identity": round(sim_identity, 4),
        "orthogonal": round(sim_orthogonal, 4),
        "opposite": round(sim_opposite, 4),
    }


# ── TODO(2): Rank against a physics query vector ─────────────────────────────
def rank_physics_query() -> list[tuple[str, float]]:
    """Rank DEMO_VECS against physics query [0.05, 0.95, 0.05]."""
    physics_query_vec = [0.05, 0.95, 0.05]
    # TODO(2): call rank_by_similarity(physics_query_vec, DEMO_VECS)
    return rank_by_similarity(physics_query_vec, DEMO_VECS)


# ── TODO(3): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Cosine similarity maps the physics query closest to Newton's laws (>0.98 similarity) "
    "and separates it from biology topics, even though both share English grammatical structures."
)


if __name__ == "__main__":
    invariants = verify_invariants()
    print("Invariants:", invariants)
    print("\nPhysics Query Rankings:")
    for text, score in rank_physics_query():
        print(f"  {score:0.4f} | {text}")
    print("\nObservation:", OBSERVATION)
