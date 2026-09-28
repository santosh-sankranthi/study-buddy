"""EXERCISE -- Hand-crafting / Simulating a ReAct Trace.

The demo simulated a 2-step ReAct trace for Biology exam preparation.
Your twist: implement a trace generator that simulates a ReAct session for:
Goal: "Calculate weighted grade for scores [80, 90, 70] with weights [0.3, 0.4, 0.3] and check Math exam date."

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/react_concept/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.tools import calculate_grade, get_exam_schedule


# ── TODO(1): Define Step 1: Grade Calculation ────────────────────────────────
def step_1_calculate_grade() -> dict:
    """Return dict with 'thought', 'action', and 'observation' for calculating grade."""
    scores = [80.0, 90.0, 70.0]
    weights = [0.3, 0.4, 0.3]
    thought = "I need to calculate the student's weighted average grade."
    action = f"calculate_grade(scores={scores}, weights={weights})"
    obs = calculate_grade(scores, weights)
    return {"thought": thought, "action": action, "observation": obs}


# ── TODO(2): Define Step 2: Exam Schedule Check ──────────────────────────────
def step_2_check_schedule() -> dict:
    """Return dict with 'thought', 'action', and 'observation' for finding the Math exam date."""
    thought = "Now I need to check when the Math exam is scheduled."
    action = "get_exam_schedule(subject='math')"
    obs = get_exam_schedule("math")
    return {"thought": thought, "action": action, "observation": obs}


# ── TODO(3): Define Step 3: Finish ───────────────────────────────────────────
def step_3_finish(obs_grade: str, obs_date: str) -> dict:
    """Return dict with 'thought' and 'action' starting with FINISH(answer=...)."""
    thought = "I have both the weighted grade and the exam date. I can present the final result."
    final_text = f"{obs_grade} {obs_date}"
    action = f"FINISH(answer='{final_text}')"
    return {"thought": thought, "action": action, "observation": None}


def run_full_trace() -> list[dict]:
    """Execute all steps and return the full trace."""
    s1 = step_1_calculate_grade()
    s2 = step_2_check_schedule()
    s3 = step_3_finish(s1["observation"], s2["observation"])
    return [s1, s2, s3]


if __name__ == "__main__":
    trace = run_full_trace()
    for i, step in enumerate(trace, 1):
        print(f"Step {i}:")
        print(f"  Thought:     {step['thought']}")
        print(f"  Action:      {step['action']}")
        print(f"  Observation: {step['observation']}")
        print()
