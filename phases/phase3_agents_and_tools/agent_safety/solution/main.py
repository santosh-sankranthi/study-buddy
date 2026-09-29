"""SOLUTION -- Agent safety: step cap and loop detection."""

MAX_STEPS = 5
ACTIONS = ["search_notes('bio')", "search_notes('bio')"]


def check_agent_safety(actions: list[str], max_steps: int = MAX_STEPS) -> tuple[bool, str, int]:
    """Return (halted, reason, executed_steps)."""
    last_action = None
    for step, action in enumerate(actions[:max_steps], 1):
        if action == last_action and last_action not in (None, "", "FINISH"):
            return True, "loop_detected", step
        if action.startswith("FINISH"):
            return False, "done", step
        last_action = action
    if len(actions) >= max_steps:
        return True, "max_steps", max_steps
    return False, "done", len(actions)


if __name__ == "__main__":
    print(check_agent_safety(ACTIONS))
