"""Reference answer: look the tool up by name and call it with the arguments."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade

TOOLS = {"calculate_grade": calculate_grade}


def call_tool(name: str, args: dict) -> str:
    """Call the registered tool `name` with the keyword arguments in `args`."""
    return TOOLS[name](**args)


if __name__ == "__main__":
    print(call_tool("calculate_grade", {"scores": [85.0, 90.0, 95.0], "weights": [0.2, 0.3, 0.5]}))
