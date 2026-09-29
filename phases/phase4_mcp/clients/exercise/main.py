"""Practice: dispatch a tool call by name through a tiny MCP-style client.

Task: finish call_tool() so it finds `name` in TOOLS and calls it with `args`.

Check your work with:
    python phases/phase4_mcp/clients/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade

TOOLS = {"calculate_grade": calculate_grade}


def call_tool(name: str, args: dict) -> str:
    """Call the registered tool `name` with the keyword arguments in `args`."""
    # TODO: look `name` up in TOOLS and call it with **args.
    raise NotImplementedError("call_tool")


if __name__ == "__main__":
    print(call_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]}))
