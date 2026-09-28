"""Self-check -- Semantic Search exercise.

Run:
    python phases/phase3_embeddings/semantic_search/solution/check.py
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

print("Checking semantic search exercise ...\n")

top_results = ex.evaluate_phrasings()
assert len(top_results) == 3, f"Expected 3 results, got {len(top_results)}"

for i, doc in enumerate(top_results):
    assert "Photosynthesis" in doc, f"Phrasing {i} failed to rank photosynthesis first. Got: {doc}"
print("✅  All 3 phrasings successfully ranked the Photosynthesis document at #1")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
