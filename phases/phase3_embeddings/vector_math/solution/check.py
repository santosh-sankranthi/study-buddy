"""Self-check -- Vector Math exercise.

Run:
    python phases/phase3_embeddings/vector_math/solution/check.py
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

print("Checking vector math exercise ...\n")

# Verify invariants
inv = ex.verify_invariants()
assert inv["identity"] == 1.0, f"Expected identity == 1.0, got {inv['identity']}"
assert inv["orthogonal"] == 0.0, f"Expected orthogonal == 0.0, got {inv['orthogonal']}"
assert inv["opposite"] == -1.0, f"Expected opposite == -1.0, got {inv['opposite']}"
print("✅  Mathematical invariants verified (identity=1.0, orthogonal=0.0, opposite=-1.0)")

# Verify physics ranking
ranked = ex.rank_physics_query()
top_text, top_score = ranked[0]
assert "Newton" in top_text or "Force" in top_text
assert top_score > 0.95
print(f"✅  Physics query correctly ranked Newton/Force at #1 (score: {top_score:.4f})")

# Verify observation
assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
