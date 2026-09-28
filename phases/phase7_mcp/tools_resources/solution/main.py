"""SOLUTION -- Expose Quiz History as an MCP Resource."""
import json

def get_quiz_attempts(session_id: str) -> str:
    return json.dumps({"session_id": session_id, "attempts": []})

if __name__ == "__main__":
    print(get_quiz_attempts("session_42"))
