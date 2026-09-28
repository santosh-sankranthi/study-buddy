"""Self-check -- Eval Frameworks exercise.

Run:
    python phases/phase9_advanced_capstone/eval_frameworks/solution/check.py
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

print("Checking eval frameworks exercise ...\n")

res = ex.evaluate_triad_suite()

assert "scores" in res and len(res["scores"]) == len(ex.TEST_RECORDS)
assert "avg_score" in res and 0.0 <= res["avg_score"] <= 1.0
assert res["scores"][0] > res["scores"][2], "Faithful case should score significantly higher than hallucinated case"
print(f"✅  Triad suite computed composite scores (avg: {res['avg_score']:0.2f})")
print(f"✅  Score discrimination verified: Case 1 ({res['scores'][0]}) > Case 3 ({res['scores'][2]})")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
