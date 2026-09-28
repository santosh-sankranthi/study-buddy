"""EXERCISE -- Multi-Guard Agent Safety Checks.

The demo caught back-to-back loop detection.
Your twist: implement check_agent_safety() evaluating actions against
MAX_STEPS and consecutive-action loop detection.

Run when done:
    python phases/phase6_agents_and_tools/agent_safety/solution/check.py
"""
# TODO(1): Implement check_agent_safety(actions: list[str], max_steps: int = 5) -> tuple[bool, str, int]
# Returns (halted: bool, reason: str, executed_steps: int)
# reasons: 'done', 'loop_detected', 'max_steps'
def check_agent_safety(actions: list[str], max_steps: int = 5) -> tuple[bool, str, int]:
    raise NotImplementedError("TODO(1): implement check_agent_safety")

# TODO(2): Write observation on deterministic guardrails
OBSERVATION = ""

if __name__ == "__main__":
    seq = ["search_notes('bio')", "search_notes('bio')"]
    print("Result:", check_agent_safety(seq, 5))
