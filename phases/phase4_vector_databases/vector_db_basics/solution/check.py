"""Self-check -- Vector DB Basics exercise.

Run:
    python phases/phase4_vector_databases/vector_db_basics/solution/check.py
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

print("Checking vector DB basics exercise ...\n")

from app.vector_store import count

c_start = count()
ids = ex.index_cs_notes()
assert len(ids) == 2, f"Expected 2 doc IDs returned, got {len(ids)}"
assert count() == c_start + 2, "Collection count should have increased by 2"
print(f"✅  Indexed 2 notes; collection count updated to {count()}")

results = ex.search_and_compute_similarity("divide and conquer sort")
assert len(results) > 0, "Expected non-empty search results"
for r in results:
    assert "similarity" in r, "Result dict missing 'similarity' key"
    assert "distance" in r, "Result dict missing 'distance' key"
    assert round(r["similarity"] + r["distance"], 2) == 1.0, "similarity + distance must equal 1.0"
print("✅  search_and_compute_similarity accurately computed similarity = 1.0 - distance")

print("\n✅  All checks passed!")
