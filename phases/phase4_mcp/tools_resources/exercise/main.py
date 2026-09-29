"""Practice: serve quiz history as a read-only MCP resource.

Task: finish get_quiz_attempts() so it returns the session's attempts as JSON.

Check your work with:
    python phases/phase4_mcp/tools_resources/solution/check.py
"""
import json

ATTEMPTS = [
    {"question": "2 + 2", "correct": True},
    {"question": "3 * 3", "correct": False},
]


def get_quiz_attempts(session_id: str) -> str:
    """Return {"session_id": session_id, "attempts": ATTEMPTS} encoded as JSON."""
    # TODO: json.dumps a dict with the session_id and the ATTEMPTS list.
    raise NotImplementedError("get_quiz_attempts")


if __name__ == "__main__":
    print(get_quiz_attempts("session_42"))
