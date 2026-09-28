"""EXERCISE -- Safe Tool Dispatching & Argument Handling.

The demo executed get_exam_schedule and handled unknown tools.
Your twist: execute calculate_grade via execute_tool_call() with scores and weights,
and test resilience against malformed JSON arguments.

Fill in every TODO. Run when done:
    python phases/phase6_agents_and_tools/function_calling_live/solution/check.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.agent import execute_tool_call


# ── TODO(1): Execute calculate_grade tool call ───────────────────────────────
def run_calculate_grade_call(scores: list[float], weights: list[float]) -> str:
    """Build tool_call dict for calculate_grade and return execute_tool_call result."""
    # TODO(1): build tool_call dict with {"function": {"name": "calculate_grade", "arguments": ...}}
    tool_call = {
        "function": {
            "name": "calculate_grade",
            "arguments": json.dumps({"scores": scores, "weights": weights}),
        }
    }
    return execute_tool_call(tool_call)


# ── TODO(2): Test handling of malformed JSON arguments ───────────────────────
def test_malformed_arguments() -> str:
    """Pass malformed arguments string and return the error message."""
    tool_call = {
        "function": {
            "name": "calculate_grade",
            "arguments": "{bad_json: missing_quotes}",
        }
    }
    # TODO(2): return execute_tool_call(tool_call)
    return execute_tool_call(tool_call)


if __name__ == "__main__":
    out = run_calculate_grade_call([85.0, 95.0], [0.5, 0.5])
    print("calculate_grade result:", out)
    err = test_malformed_arguments()
    print("malformed arguments result:", err)
