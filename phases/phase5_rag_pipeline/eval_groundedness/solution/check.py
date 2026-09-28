"""Self-check -- Eval Groundedness exercise.

Run:
    python phases/phase5_rag_pipeline/eval_groundedness/solution/check.py
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

print("Checking eval groundedness exercise ...\n")

results = ex.evaluate_rag_test_suite()
assert len(results) == 3, f"Expected 3 test results, got {len(results)}"

# Map results by id
by_id = {r["id"]: r for r in results}

# Check grounded_valid
assert by_id["grounded_valid"]["det_passed"] is True
assert by_id["grounded_valid"]["grounded_passed"] is True
print("✅  grounded_valid passed both deterministic and groundedness checks")

# Check missing_citation
assert by_id["missing_citation"]["det_passed"] is False
print("✅  missing_citation correctly failed the deterministic citation check")

# Check hallucination
assert by_id["hallucination"]["grounded_passed"] is False
print("✅  hallucination correctly flagged as ungrounded")

print("\n✅  All checks passed!")
