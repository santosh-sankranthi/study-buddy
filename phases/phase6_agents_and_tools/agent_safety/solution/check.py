"""Self-check -- Agent Safety exercise.

Run:
    python phases/phase6_agents_and_tools/agent_safety/solution/check.py
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

print("Checking agent safety exercise ...\n")

# Test 1: Normal finish
halted, reason, steps = ex.check_agent_safety(["step_1", "FINISH"], max_steps=5)
assert halted is False and reason == "done" and steps == 2
print("✅  Normal completion identified correctly")

# Test 2: Consecutive action loop
halted, reason, steps = ex.check_agent_safety(["search('a')", "search('a')"], max_steps=5)
assert halted is True and reason == "loop_detected" and steps == 2
print("✅  Consecutive action loop intercepted at step 2")

# Test 3: Max steps ceiling
halted, reason, steps = ex.check_agent_safety([f"step_{i}" for i in range(10)], max_steps=4)
assert halted is True and reason == "max_steps" and steps == 4
print("✅  MAX_STEPS ceiling halted long running agent at step 4")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
