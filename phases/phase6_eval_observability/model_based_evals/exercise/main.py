"""EXERCISE -- LLM-as-a-Judge.

Practice: ask the model to score an answer against a written rubric.
Task: finish evaluate_tone() so it sends TONE_CRITERIA and the answer to the
model and returns {"score": int, "reason": str}.

Check your work with:
    python phases/phase6_eval_observability/model_based_evals/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

TONE_CRITERIA = (
    "Score the pedagogical tone from 1 (harsh and unhelpful) to 5 "
    "(warm, patient, encouraging). Reply with the number and a short reason."
)


def parse_score(reply: str) -> int:
    """Return the first 1-5 integer in `reply`, or 0 if there is none."""
    # TODO: return the first number 1-5 found in reply, else 0.
    raise NotImplementedError("parse_score")


def evaluate_tone(answer: str) -> dict:
    """Score `answer` with the model and return {"score", "reason"}."""
    # TODO: build the messages, call chat(messages, temperature=0.0), parse it.
    raise NotImplementedError("evaluate_tone")


if __name__ == "__main__":
    print(evaluate_tone("Great question! What do you think chlorophyll does?"))
