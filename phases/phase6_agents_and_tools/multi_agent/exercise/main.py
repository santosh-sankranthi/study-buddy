"""EXERCISE -- Multi-Agent Orchestration & Quality Control.

The demo evaluated planner and critic roles independently.
Your twist: execute the complete plan_and_execute() pipeline, verify that the
planner emits bounded steps (1 <= steps <= 5), that critic evaluations are
recorded for each step, and that a synthesized final answer is produced.

Fill in every TODO. Run when done:
    python phases/phase6_agents_and_tools/multi_agent/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import critic, plan_and_execute, planner


# ── TODO(1): Verify planner step bounds ───────────────────────────────────────
def verify_planner_output(goal: str) -> list[str]:
    """Call planner(goal) and assert 1 <= len(plan) <= 5."""
    # TODO(1): plan = planner(goal); return plan
    return planner(goal)


# ── TODO(2): Test critic discrimination ──────────────────────────────────────
def test_critic_quality_gate() -> tuple[bool, bool]:
    """Return (approved_good, approved_bad) using critic()."""
    step = "Find Math exam schedule"
    # TODO(2): evaluate a good answer vs an empty error string
    good_ans = "The Math exam is on 2026-11-01."
    bad_ans = ""
    app_good, _ = critic(step, good_ans)
    app_bad, _ = critic(step, bad_ans)
    return app_good, app_bad


# ── TODO(3): Run full plan_and_execute ───────────────────────────────────────
def run_orchestration(goal: str) -> dict:
    """Execute plan_and_execute(goal) and return result dictionary."""
    # TODO(3): return plan_and_execute(goal)
    return plan_and_execute(goal)


if __name__ == "__main__":
    test_goal = "Look up exam date for Math and search for calculus review notes."
    p = verify_planner_output(test_goal)
    print(f"Generated {len(p)} steps:", p)
    g, b = test_critic_quality_gate()
    print(f"Critic: good={g}, bad={b}")
    res = run_orchestration(test_goal)
    print("\nFinal Answer:", res["final_answer"])
