"""SOLUTION -- Agent loops: detect a repeated tool call."""

CALLS = [
    {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
    {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
]


def detect_repetition(tool_calls: list[dict]) -> bool:
    """Return True if the final tool call equals the one before it."""
    if len(tool_calls) < 2:
        return False
    return tool_calls[-1] == tool_calls[-2]


if __name__ == "__main__":
    print("Repeated:", detect_repetition(CALLS))
