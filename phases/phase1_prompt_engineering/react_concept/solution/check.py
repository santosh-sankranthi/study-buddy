"""Self-check -- ReAct concept exercise.

Run:
    python phases/phase1_prompt_engineering/react_concept/solution/check.py
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

print("Checking ReAct concept exercise ...\n")

trace = ex.run_full_trace()
assert len(trace) == 3, f"Expected 3 steps in trace, got {len(trace)}"
print("✅  Trace has 3 steps")

# Check step 1
s1 = trace[0]
assert "calculate_grade" in s1["action"]
assert "81.00%" in s1["observation"]
print("✅  Step 1 correctly invokes calculate_grade and yields 81.00%")

# Check step 2
s2 = trace[1]
assert "get_exam_schedule" in s2["action"]
assert "2026-11-01" in s2["observation"]
print("✅  Step 2 correctly invokes get_exam_schedule and yields 2026-11-01")

# Check step 3
s3 = trace[2]
assert s3["action"].startswith("FINISH(")
print("✅  Step 3 action starts with FINISH(")

print("\n✅  All checks passed!")
