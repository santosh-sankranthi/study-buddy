"""EXERCISE -- Same-Tool Loop Detection.

The demo capped iterations at MAX_STEPS. Your twist: implement loop detection
so that if the same tool is called with identical arguments twice in a row,
the loop halts immediately with reason='loop_detected'.

Run when done:
    python phases/phase6_agents_and_tools/agent_loops/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement loop_detector(history: list[dict]) -> bool
#   Given a list of tool calls [{'name': str, 'arguments': str}],
#   return True if the last tool call is identical to the preceding one.

def detect_repetition(tool_calls: list[dict]) -> bool:
    raise NotImplementedError("TODO(1): implement detect_repetition")


# TODO(2): Write one sentence explaining why loop detection is critical in production:
OBSERVATION = ""


if __name__ == "__main__":
    sample_calls = [
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
        {"name": "search_notes", "arguments": '{"query": "mitosis"}'},
    ]
    print("Repetition detected:", detect_repetition(sample_calls))
