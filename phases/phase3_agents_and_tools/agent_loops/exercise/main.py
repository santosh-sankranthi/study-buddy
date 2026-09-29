"""EXERCISE -- Agent loops: detect a repeated tool call.

Practice: stop an agent that calls the same tool with the same arguments twice.

Task: finish detect_repetition() so it reports whether the last two calls match.

Check your work with:
    python phases/phase3_agents_and_tools/agent_loops/solution/check.py
"""

CALLS = [
    {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
    {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
]


def detect_repetition(tool_calls: list[dict]) -> bool:
    """Return True if the final tool call equals the one before it."""
    # TODO: compare tool_calls[-1] with tool_calls[-2]; return False for < 2 calls.
    raise NotImplementedError("detect_repetition")


if __name__ == "__main__":
    print("Repeated:", detect_repetition(CALLS))
