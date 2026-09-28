"""DEMO -- Vector Representations & Cosine Similarity.

Live-code target: inspect hand-rolled cosine_similarity() in app.embeddings,
rank 3-D toy vectors against a query vector, and observe how semantic closeness
maps directly to mathematical proximity.

Run:
    python phases/phase3_embeddings/vector_math/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import DEMO_VECS, cosine_similarity, rank_by_similarity

print("=" * 60)
print("VECTOR MATHEMATICS & COSINE SIMILARITY DEMO")
print("=" * 60)

# Query vector: heavily weighted towards photosynthesis/plants
query_text = "Query: How do plants convert sunlight?"
query_vec = [0.85, 0.15, 0.15]

print(f"\n{query_text}")
print(f"Query Vector: {query_vec}\n")

# Rank all candidate texts
ranked = rank_by_similarity(query_vec, DEMO_VECS)

print(f"{'Similarity':>10} | Candidate Sentence")
print("-" * 60)
for text, score in ranked:
    print(f"{score:>10.4f} | {text}")

print("\nProperties Verification:")
v1 = [1.0, 2.0, 3.0]
v_ortho = [-2.0, 1.0, 0.0]  # dot product = -2 + 2 + 0 = 0
print(f"  Self-similarity (v · v):            {cosine_similarity(v1, v1):.4f} (Expected: 1.0)")
print(f"  Orthogonal vectors:                {cosine_similarity(v1, v_ortho):.4f} (Expected: 0.0)")
