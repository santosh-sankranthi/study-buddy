"""EXERCISE -- Few-Shot / Zero-Shot.

Practice: two examples show the model the output format you want.

Task: fill in MY_EXAMPLES and messages_for().

Check your work with:
    python phases/phase1_prompt_engineering/few_shot_zero_shot/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.prompts import build_few_shot_prompt  # noqa: E402

# TODO(1): two examples, each a dict {"input": <topic>, "output": <fill-in-the-blank>}
MY_EXAMPLES: list[dict] = []


def messages_for(topic: str) -> list[dict]:
    """Return the few-shot messages for `topic`."""
    # TODO(2): build them from MY_EXAMPLES with build_few_shot_prompt().
    raise NotImplementedError("messages_for")


if __name__ == "__main__":
    print(messages_for("The Calvin cycle"))
