"""EXERCISE -- Batch Embedding Generation & Similarity Comparison.

The demo embedded 3 sentences using embed_batch().
Your twist: embed a list of 5 sentences across two subjects (Biology and Physics),
verify that batch embedding preserves ordering, and verify that subject-internal
pairs exhibit higher cosine similarity than cross-subject pairs.

Fill in every TODO. Run when done:
    python phases/phase3_embeddings/embedding_api/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import cosine_similarity, embed_batch

SENTENCES = [
    "Photosynthesis converts sunlight into glucose.",            # Bio 1
    "Plants use chloroplasts to capture radiant energy.",        # Bio 2
    "Newton's laws of motion govern classical mechanics.",      # Phys 1
    "Force equals mass multiplied by acceleration.",             # Phys 2
    "Thermodynamics dictates heat flows from hot to cold.",      # Phys 3
]


# ── TODO(1): Embed all sentences in a single batch ───────────────────────────
def get_sentence_embeddings() -> list[list[float]]:
    """Return list of embedding vectors using embed_batch(SENTENCES)."""
    # TODO(1): return embed_batch(SENTENCES)
    return embed_batch(SENTENCES)


# ── TODO(2): Compare similarities ────────────────────────────────────────────
def compare_similarities(vecs: list[list[float]]) -> tuple[float, float]:
    """Compute:

    1. sim_bio: similarity between Bio 1 and Bio 2 (vecs[0], vecs[1])
    2. sim_cross: similarity between Bio 1 and Phys 1 (vecs[0], vecs[2])
    Returns (sim_bio, sim_cross).
    """
    # TODO(2): compute sim_bio and sim_cross
    sim_bio = cosine_similarity(vecs[0], vecs[1])
    sim_cross = cosine_similarity(vecs[0], vecs[2])
    return round(sim_bio, 4), round(sim_cross, 4)


if __name__ == "__main__":
    vecs = get_sentence_embeddings()
    print(f"Generated {len(vecs)} vectors with {len(vecs[0])} dimensions.")
    sim_bio, sim_cross = compare_similarities(vecs)
    print(f"Bio ↔ Bio Similarity:     {sim_bio}")
    print(f"Bio ↔ Phys Similarity:    {sim_cross}")
