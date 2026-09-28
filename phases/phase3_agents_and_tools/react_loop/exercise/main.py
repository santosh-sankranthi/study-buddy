"""EXERCISE -- Multi-Tool Sequence Tracing.

The demo traced a single tool step.
Your twist: ask a question that requires TWO tools in sequence
(e.g., looking up the biology exam date AND searching notes for biology exam topics).

Run when done:
    python phases/phase3_agents_and_tools/react_loop/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Provide a multi-tool query string
TWO_TOOL_QUESTION = ""

# TODO(2): Write one sentence describing why sequential tool calling is essential:
OBSERVATION = ""

if __name__ == "__main__":
    print("Question:", TWO_TOOL_QUESTION)
    print("Observation:", OBSERVATION)
