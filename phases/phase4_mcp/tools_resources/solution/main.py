"""Reference answer: read the attempt list and encode it as a JSON resource."""
import json

ATTEMPTS = [
    {"question": "2 + 2", "correct": True},
    {"question": "3 * 3", "correct": False},
]


def get_quiz_attempts(session_id: str) -> str:
    """Return {"session_id": session_id, "attempts": ATTEMPTS} encoded as JSON."""
    return json.dumps({"session_id": session_id, "attempts": ATTEMPTS})


if __name__ == "__main__":
    print(get_quiz_attempts("session_42"))
