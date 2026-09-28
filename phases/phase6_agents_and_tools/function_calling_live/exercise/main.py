"""EXERCISE -- Live Function Execution: calculate_grade.

The demo dispatched get_exam_schedule.
Your twist: implement dispatch_grade_tool(scores: list[float], weights: list[float]) -> str
and verify that execute_tool_call() properly executes the calculation.

Run when done:
    python phases/phase6_agents_and_tools/function_calling_live/solution/check.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import execute_tool_call

# TODO(1): Implement dispatch_grade_tool(scores: list[float], weights: list[float]) -> str
# Construct a tool_call dict:
# {
#     "function": {
#         "name": "calculate_grade",
#         "arguments": json.dumps({"scores": scores, "weights": weights})
#     }
# }
# Return the result of execute_tool_call(tool_call)

def dispatch_grade_tool(scores: list[float], weights: list[float]) -> str:
    raise NotImplementedError("TODO(1): implement dispatch_grade_tool")

if __name__ == "__main__":
    print(dispatch_grade_tool([80.0, 90.0, 70.0], [0.3, 0.4, 0.3]))
