"""Practice: how many words of notes fit in a token budget?
Task: finish note_budget_words() using the fixed setup below.
Check your work with: python phases/phase0_fundamentals/context_window/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

SYSTEM_PROMPT = "You are Study Buddy, a patient tutor. Answer only from the student's notes."
# The 5 previous turns, each as (user_message, assistant_reply).
HISTORY = [
    ("What is photosynthesis?", "It converts light into chemical energy."),
    ("Where does it happen?", "In the chloroplasts of plant cells."),
    ("What pigment absorbs light?", "Chlorophyll, mostly red and blue light."),
    ("What gas is released?", "Oxygen, from splitting water."),
    ("What is the Calvin cycle?", "The light-independent stage that fixes CO2."),
]
REPLY_RESERVE_TOKENS = 400  # room the model needs for its own reply
CONTEXT_BUDGET = 8000  # total tokens for this one call, input plus output
WORDS_PER_TOKEN = 0.75  # crude way to turn leftover tokens into words


def tokens_used_so_far() -> int:
    """Tokens taken by the system prompt plus all 5 history turns."""
    total = count_tokens(SYSTEM_PROMPT)
    for question, answer in HISTORY:
        total += count_tokens(question) + count_tokens(answer)
    return total


def note_budget_words() -> int:
    """How many words of notes fit after the reply reserve.

    TODO: subtract REPLY_RESERVE_TOKENS and tokens_used_so_far() from
    CONTEXT_BUDGET, floor the leftover tokens times WORDS_PER_TOKEN, and
    return 0 if the leftover is negative.
    """
    raise NotImplementedError("note_budget_words")


if __name__ == "__main__":
    print("fixed tokens used:", tokens_used_so_far())
    print("note words that fit:", note_budget_words())
