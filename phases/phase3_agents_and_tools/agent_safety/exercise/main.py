"""EXERCISE -- Agent safety: step cap and loop detection.

Practice: halt a runaway agent before it burns tokens.

Task: finish check_agent_safety() so it returns (halted, reason, steps).

Check your work with:
    python phases/phase3_agents_and_tools/agent_safety/solution/check.py
"""

MAX_STEPS = 5
ACTIONS = ["search_notes('bio')", "search_notes('bio')"]


def check_agent_safety(actions: list[str], max_steps: int = MAX_STEPS) -> tuple[bool, str, int]:
    """Return (halted, reason, executed_steps).

    reasons: 'done' when a FINISH action or the actions run out, 'loop_detected'
    when the same action repeats back-to-back, 'max_steps' when the cap is hit.
    """
    # TODO: walk the actions up to max_steps, tracking the previous action.
    raise NotImplementedError("check_agent_safety")


if __name__ == "__main__":
    print(check_agent_safety(ACTIONS))
