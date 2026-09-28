"""EXERCISE -- Wire calculate_grade into TOOL_REGISTRY.

The demo registered search_notes and get_exam_schedule.
Your twist: implement calculate_grade and wire it into TOOL_REGISTRY.

Run when done:
    python phases/phase6_agents_and_tools/tools/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): In app/tools.py (or implement below for self-check):
#   Implement calculate_grade(scores: list[float], weights: list[float]) -> str
#   - Check that len(scores) == len(weights)
#   - Calculate weighted average: sum(s * w) / sum(w)
#   - Return string: "Weighted average: <grade>%"

def calculate_grade(scores: list[float], weights: list[float]) -> str:
    raise NotImplementedError("TODO(1): implement calculate_grade")


# TODO(2): Register calculate_grade in TOOL_REGISTRY
# TOOL_REGISTRY["calculate_grade"] = calculate_grade


if __name__ == "__main__":
    scores = [80.0, 90.0, 70.0]
    weights = [0.3, 0.4, 0.3]
    result = calculate_grade(scores, weights)
    print("Calculated grade:", result)
