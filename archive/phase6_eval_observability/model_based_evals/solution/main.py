"""SOLUTION -- LLM-as-a-Judge.

Reference answer: send a rubric prompt to the model and parse its score.
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
    for word in reply.split():
        if word.isdigit() and 1 <= int(word) <= 5:
            return int(word)
    return 0


def evaluate_tone(answer: str) -> dict:
    """Score `answer` with the model and return {"score", "reason"}."""
    messages = [
        {"role": "system", "content": TONE_CRITERIA},
        {"role": "user", "content": answer},
    ]
    reply = chat(messages, temperature=0.0)
    return {"score": parse_score(reply), "reason": reply.strip()}


if __name__ == "__main__":
    print(evaluate_tone("Great question! What do you think chlorophyll does?"))
