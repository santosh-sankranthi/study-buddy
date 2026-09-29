"""Reference answer: store calculate_grade in the server's tool table."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade

SERVER_TOOLS: dict = {}


def register_grade_tool(server: dict) -> bool:
    """Store calculate_grade in `server`; return True once it is registered."""
    server["calculate_grade"] = calculate_grade
    return True


if __name__ == "__main__":
    print("Registered:", register_grade_tool(SERVER_TOOLS))
