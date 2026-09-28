"""EXERCISE -- Expose Quiz History as an MCP Resource.

The demo exposed notes://corpus.
Your twist: expose a session quiz history resource at 'quiz://attempts/{session_id}'.

Run when done:
    python phases/phase4_mcp/tools_resources/solution/check.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement get_quiz_attempts(session_id: str) -> str
#   Return a JSON-encoded dict with {"session_id": session_id, "attempts": []}

def get_quiz_attempts(session_id: str) -> str:
    raise NotImplementedError("TODO(1): implement get_quiz_attempts")


if __name__ == "__main__":
    res = get_quiz_attempts("session_42")
    print("Quiz resource output:", res)
