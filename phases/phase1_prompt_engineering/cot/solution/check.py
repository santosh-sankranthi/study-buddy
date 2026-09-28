"""Self-check -- CoT exercise.

Run:
    python phases/phase1_prompt_engineering/cot/solution/check.py
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

print("Checking cot exercise ...\n")

assert hasattr(ex, "results_no_cot") and len(ex.results_no_cot) == 3, \
    "results_no_cot must have 3 entries."
print("✅  results_no_cot has 3 entries")

assert hasattr(ex, "results_cot") and len(ex.results_cot) == 3, \
    "results_cot must have 3 entries."
print("✅  results_cot has 3 entries")

assert all(isinstance(r, str) and r for r in ex.results_no_cot), "All results must be strings."
assert all(isinstance(r, str) and r for r in ex.results_cot),    "All results must be strings."
print("✅  All results are non-empty strings")

assert isinstance(ex.OBSERVATION, str) and len(ex.OBSERVATION.strip()) > 20, \
    "OBSERVATION must be > 20 chars."
print("✅  OBSERVATION is filled in")

print("\n✅  All checks passed!")
