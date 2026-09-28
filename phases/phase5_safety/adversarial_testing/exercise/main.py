"""EXERCISE -- Red-Teaming the Agent Loop.

Write 3 adversarial test cases that verify the agent defends against:
1. Infinite loop attacks
2. Unauthorized tool calls
3. Tool result jailbreaks

Run when done:
    python phases/phase5_safety/adversarial_testing/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement run_redteam_tests() -> dict[str, bool]
# Return a dict mapping test names to True (if test defended successfully)

def run_redteam_tests() -> dict[str, bool]:
    raise NotImplementedError("TODO(1): implement run_redteam_tests")


if __name__ == "__main__":
    print("Test outcomes:", run_redteam_tests())
