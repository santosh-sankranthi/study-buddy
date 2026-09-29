"""SOLUTION -- Multi-agent: a critic checks the result."""

STEP = "Find the biology exam date."
GOOD = "Biology exam is scheduled for 2026-11-15."
BAD = ""


def critic(step: str, result: str) -> tuple[bool, str]:
    """Return (approved, reason)."""
    if len(result.strip()) < 10 or "error" in result.lower():
        return False, "Result is empty, too brief, or contains an error."
    return True, "Result adequately addresses the step."


if __name__ == "__main__":
    print(critic(STEP, GOOD))
    print(critic(STEP, BAD))
