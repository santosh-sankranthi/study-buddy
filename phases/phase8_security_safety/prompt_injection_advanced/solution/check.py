"""Self-check -- Advanced Prompt Injection exercise.

Run:
    python phases/phase8_security_safety/prompt_injection_advanced/solution/check.py
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

print("Checking advanced prompt injection exercise ...\n")

results = ex.scan_batch_for_injections()
assert len(results) == len(ex.TEST_MATRIX)

for r in results:
    assert r["expected"] == r["flagged"], f"Classification error for: {r['text']!r} (expected {r['expected']}, got {r['flagged']})"
    if r["flagged"]:
        assert "[BLOCKED]" in r["clean"]
print("✅  All test matrix cases correctly classified with zero false positives or false negatives")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
