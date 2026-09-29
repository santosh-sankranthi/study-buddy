"""Practice: expose calculate_grade as a tool on a tiny MCP-style server.

Task: finish register_grade_tool() so it stores calculate_grade under its name.

Check your work with:
    python phases/phase4_mcp/servers/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade

SERVER_TOOLS: dict = {}


def register_grade_tool(server: dict) -> bool:
    """Store calculate_grade in `server`; return True once it is registered."""
    # TODO: put calculate_grade into `server` under the key "calculate_grade".
    raise NotImplementedError("register_grade_tool")


if __name__ == "__main__":
    print("Registered:", register_grade_tool(SERVER_TOOLS))
