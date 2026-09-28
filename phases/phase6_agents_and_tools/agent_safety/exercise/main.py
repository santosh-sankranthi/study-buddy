"""EXERCISE -- Building Multi-Guard Agent Safety Checks.

The demo caught back-to-back loop detection.
Your twist: implement check_agent_safety() to evaluate arbitrary action streams
against both MAX_STEPS caps and consecutive-action loop detection, and verify
against test sequences.

Fill in every TODO. Run when done:
    python phases/phase6_agents_and_tools/agent_safety/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))


# ── TODO(1): Implement check_agent_safety ────────────────────────────────────
def check_agent_safety(
    actions: list[str],
    max_steps: int = 5,
) -> tuple[bool, str, int]:
    """Evaluate an action sequence.

    Returns:
        (halted: bool, reason: str, executed_steps: int)
        Reasons: 'done', 'loop_detected', 'max_steps'
    """
    last_action = None
    # TODO(1): iterate over actions up to max_steps:
    #   if action == last_action: return True, "loop_detected", step
    #   if action.startswith("FINISH"): return False, "done", step
    #   last_action = action
    # if loop completes without finish: return True, "max_steps", max_steps
    for step, action in enumerate(actions[:max_steps], 1):
        if action == last_action and last_action not in (None, "", "FINISH"):
            return True, "loop_detected", step
        if action.startswith("FINISH"):
            return False, "done", step
        last_action = action

    if len(actions) >= max_steps:
        return True, "max_steps", max_steps

    return False, "done", len(actions)


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Guardrails provide deterministic bounds on stochastic agent behavior, "
    "preventing infinite recursion and bounding maximum API expenditure."
)


if __name__ == "__main__":
    seq_normal = ["search_notes('bio')", "FINISH(answer='Photosynthesis')"]
    seq_loop = ["search_notes('bio')", "search_notes('bio')"]
    seq_long = [f"step_{i}" for i in range(10)]

    print("Normal: ", check_agent_safety(seq_normal, max_steps=5))
    print("Loop:   ", check_agent_safety(seq_loop, max_steps=5))
    print("Long:   ", check_agent_safety(seq_long, max_steps=5))
    print("\nObservation:", OBSERVATION)
