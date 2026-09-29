"""SOLUTION -- ReAct Trace."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade, get_exam_schedule  # noqa: E402

SCORES = [80.0, 90.0, 70.0]
WEIGHTS = [0.3, 0.4, 0.3]


def run_full_trace() -> list[dict]:
    grade = calculate_grade(SCORES, WEIGHTS)
    date = get_exam_schedule("math")
    return [
        {"thought": "I need the weighted average grade.",
         "action": f"calculate_grade({SCORES}, {WEIGHTS})", "observation": grade},
        {"thought": "Now I need the Math exam date.",
         "action": "get_exam_schedule('math')", "observation": date},
        {"thought": "I have both results.",
         "action": f"FINISH(answer='{grade} {date}')", "observation": None},
    ]


if __name__ == "__main__":
    for step in run_full_trace():
        print(step)
