"""EXERCISE -- Multi-agent: a critic checks the result.

Practice: a critic decides whether an executor's result is good enough.

Task: finish critic() so it approves useful results and rejects weak ones.

Check your work with:
    python phases/phase3_agents_and_tools/multi_agent/solution/check.py
"""

STEP = "Find the biology exam date."
GOOD = "Biology exam is scheduled for 2026-11-15."
BAD = ""


def critic(step: str, result: str) -> tuple[bool, str]:
    """Return (approved, reason); reject empty results or ones containing 'error'."""
    # TODO: return (False, reason) for weak results, (True, reason) otherwise.
    raise NotImplementedError("critic")


if __name__ == "__main__":
    print(critic(STEP, GOOD))
    print(critic(STEP, BAD))
