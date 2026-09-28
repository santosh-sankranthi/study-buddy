"""Self-check -- Retrieval exercise.

Run:
    python phases/phase5_rag_pipeline/retrieval/solution/check.py
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

print("Checking retrieval exercise ...\n")

counts = ex.evaluate_thresholds()
assert 0.10 in counts and 0.35 in counts and 0.95 in counts
assert counts[0.10] >= counts[0.35], "Looser threshold should return >= chunks than balanced"
assert counts[0.35] >= counts[0.95], "Balanced threshold should return >= chunks than strict"
print(f"✅  Monotonicity verified across thresholds: {counts}")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
