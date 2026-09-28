"""EXERCISE -- Multi-Agent Critic Verification.

The demo implemented Planner -> Executor.
Your twist: implement a Critic function that evaluates an executor output
and returns (approved: bool, reason: str).

Run when done:
    python phases/phase3_agents_and_tools/multi_agent/solution/check.py
"""
# TODO(1): Implement critic(step: str, result: str) -> tuple[bool, str]
# Return (True, "Good") if result contains relevant info and is non-empty;
# otherwise return (False, "Needs more detail").
def critic(step: str, result: str) -> tuple[bool, str]:
    raise NotImplementedError("TODO(1): implement critic")

if __name__ == "__main__":
    print(critic("Find exam date", "Biology exam is on 2026-11-15."))
