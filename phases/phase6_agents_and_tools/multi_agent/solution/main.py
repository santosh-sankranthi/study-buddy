"""SOLUTION -- Multi-Agent Critic Verification."""
def critic(step: str, result: str) -> tuple[bool, str]:
    if not result or len(result.strip()) < 10 or "error" in result.lower():
        return False, "Result is too brief or contains an error."
    return True, "Approved: adequately addresses the requested step."

if __name__ == "__main__":
    print(critic("Find exam date", "Biology exam is on 2026-11-15."))
