"""Self-check -- Embedding API exercise.

Run:
    python phases/phase3_embeddings/embedding_api/solution/check.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

spec = importlib.util.spec_from_file_location(
    "ex", Path(__file__).resolve().parents[1] / "exercise" / "main.py"
)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

print("Checking embedding API exercise ...\n")

# Verify embeddings
vecs = ex.get_sentence_embeddings()
assert len(vecs) == len(ex.SENTENCES), f"Expected {len(ex.SENTENCES)} vectors, got {len(vecs)}"
dim = len(vecs[0])
assert dim >= 64, f"Vector dimension too small: {dim}"
assert all(len(v) == dim for v in vecs), "All vectors must have identical dimensions"
print(f"✅  embed_batch produced {len(vecs)} vectors of dimension {dim}")

# Verify similarities
sim_bio, sim_cross = ex.compare_similarities(vecs)
assert sim_bio > sim_cross, f"Expected sim_bio ({sim_bio}) > sim_cross ({sim_cross})"
print(f"✅  Topic similarity behaves correctly: Bio↔Bio ({sim_bio}) > Bio↔Phys ({sim_cross})")

print("\n✅  All checks passed!")
