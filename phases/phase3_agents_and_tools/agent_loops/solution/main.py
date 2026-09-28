"""SOLUTION -- Same-Tool Loop Detection."""
def detect_repetition(tool_calls: list[dict]) -> bool:
    if len(tool_calls) < 2:
        return False
    prev = tool_calls[-2]
    curr = tool_calls[-1]
    return (prev.get("name") == curr.get("name")) and (prev.get("arguments") == curr.get("arguments"))

OBSERVATION = "Loop detection prevents infinite recursive API calls and quota depletion when models hallucinate stagnant reasoning loops."

if __name__ == "__main__":
    calls = [
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
    ]
    print("Detected:", detect_repetition(calls))
