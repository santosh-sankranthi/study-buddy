"""Self-check -- ReAct Loop exercise.

Run:
    python phases/phase6_agents_and_tools/react_loop/solution/check.py
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

print("Checking ReAct loop exercise ...\n")

res = ex.run_biology_query()
assert "answer" in res and res["answer"], "Expected non-empty answer in result"
assert "steps" in res and res["steps"] >= 1, "Agent should complete in at least 1 step"
assert res.get("halted") is False, "Agent should complete cleanly without halting"
print(f"✅  agent_loop finished successfully in {res['steps']} step(s)")

# Validate trace
valid_trace = ex.validate_trace_structure(res)
assert valid_trace is True, "Trace steps missing required keys"
print(f"✅  Execution trace conforms to Thought/Action/Observation schema ({len(res['trace'])} records)")

print("\n✅  All checks passed!")
