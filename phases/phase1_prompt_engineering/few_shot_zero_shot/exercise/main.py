"""EXERCISE -- Few-Shot: Fill-in-the-blank style questions.

The demo built a quiz generator with 2 MCQ examples.
Your twist: provide 2 new examples in MY_EXAMPLES that produce a
FILL-IN-THE-BLANK style question (e.g. '_____ is the powerhouse of the cell').

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/few_shot_zero_shot/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.prompts import build_few_shot_prompt

# TODO(1): Provide 2 examples with 'input' (topic) and 'output' (fill-in-the-blank question).
MY_EXAMPLES: list[dict] = []

def generate_fill_in_the_blank(topic: str) -> str:
    """Build few-shot messages and call chat()."""
    # TODO(2): Call build_few_shot_prompt(MY_EXAMPLES, topic) and pass to chat().
    raise NotImplementedError("TODO(2): implement generate_fill_in_the_blank")

if __name__ == "__main__":
    topic = "The Calvin cycle"
    result = generate_fill_in_the_blank(topic)
    print("Result for", topic, ":\n", result)
