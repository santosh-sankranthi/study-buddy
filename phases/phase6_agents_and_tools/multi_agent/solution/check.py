"""Self-check -- Multi-Agent exercise.

Run:
    python phases/phase6_agents_and_tools/multi_agent/solution/check.py
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

print("Checking multi-agent exercise ...\n")

goal = "Review Biology exam requirements and calculate minimum passing score."

# Check planner
plan = ex.verify_planner_output(goal)
assert 1 <= len(plan) <= 5, f"Expected 1 to 5 steps, got {len(plan)}"
print(f"✅  planner emitted {len(plan)} structured steps")

# Check critic
app_good, app_bad = ex.test_critic_quality_gate()
assert app_good is True, "Critic should approve valid informative answer"
assert app_bad is False, "Critic should reject empty/insufficient answer"
print("✅  critic correctly discriminated between valid and failing results")

# Check full orchestration
res = ex.run_orchestration(goal)
assert "plan" in res and "results" in res and "final_answer" in res
assert len(res["results"]) == len(res["plan"])
print(f"✅  plan_and_execute orchestrated {len(res['plan'])} steps to final synthesis")

print("\n✅  All checks passed!")
