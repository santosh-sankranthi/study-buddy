"""DEMO -- Real Embedding API & Batch Processing.

Live-code target: call embed() and embed_batch() from app.embeddings,
inspect vector dimensions, and observe batching efficiency.

Run:
    python phases/phase3_embeddings/embedding_api/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import embed, embed_batch

print("=" * 60)
print("EMBEDDING API & BATCHING DEMO")
print("=" * 60)

# Single embedding
sample_text = "Mitochondria produce ATP through oxidative phosphorylation."
vec = embed(sample_text)
print(f"\nSingle Embed Input: '{sample_text}'")
print(f"Vector Dimensions:   {len(vec)}")
print(f"First 5 coordinates: {[round(x, 4) for x in vec[:5]]}")

# Batch embedding
batch_texts = [
    "Photosynthesis occurs in plant chloroplasts.",
    "Cellular respiration occurs in mitochondria.",
    "DNA replication occurs in the nucleus.",
]
print(f"\nEmbedding batch of {len(batch_texts)} sentences...")
batch_vecs = embed_batch(batch_texts)
print(f"Batch returned {len(batch_vecs)} vectors, each with {len(batch_vecs[0])} dimensions.")
