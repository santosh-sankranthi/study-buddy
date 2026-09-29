"""EXERCISE -- ReAct Trace.

Practice: a ReAct trace is a list of thought -> action -> observation steps.

Task: fill in run_full_trace().

Check your work with:
    python phases/phase1_prompt_engineering/react_concept/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade, get_exam_schedule  # noqa: E402

SCORES = [80.0, 90.0, 70.0]
WEIGHTS = [0.3, 0.4, 0.3]


def run_full_trace() -> list[dict]:
    """Return 3 steps: calculate the grade, check the math exam date, then FINISH."""
    # TODO: each step is {"thought", "action", "observation"}; the last has no observation.
    raise NotImplementedError("run_full_trace")


if __name__ == "__main__":
    for step in run_full_trace():
        print(step)
