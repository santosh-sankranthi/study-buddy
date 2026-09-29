"""EXERCISE -- Function calling: run the model's tool call.

Practice: a tool call is JSON the model emits; you parse it and run real code.

Task: finish dispatch_grade_tool() so it executes through execute_tool_call().

Check your work with:
    python phases/phase3_agents_and_tools/function_calling_live/solution/check.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import execute_tool_call

SCORES = [80.0, 90.0, 70.0]
WEIGHTS = [0.3, 0.4, 0.3]


def dispatch_grade_tool(scores: list[float], weights: list[float]) -> str:
    """Build a calculate_grade tool call and return the executed result."""
    # TODO: tool_call = {"function": {"name": "calculate_grade",
    #     "arguments": json.dumps({"scores": scores, "weights": weights})}}
    # then return execute_tool_call(tool_call).
    raise NotImplementedError("dispatch_grade_tool")


if __name__ == "__main__":
    print(dispatch_grade_tool(SCORES, WEIGHTS))
