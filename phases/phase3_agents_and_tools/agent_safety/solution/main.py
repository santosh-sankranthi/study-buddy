"""SOLUTION -- Multi-Guard Agent Safety Checks."""
def check_agent_safety(actions: list[str], max_steps: int = 5) -> tuple[bool, str, int]:
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

OBSERVATION = "Deterministic guardrails protect user quota and prevent unbounded inference recursion."

if __name__ == "__main__":
    print(check_agent_safety(["search", "search"]))
