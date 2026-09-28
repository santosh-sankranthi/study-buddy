"""EXERCISE -- Context Windows (your twist).

The demo grew a request until it overflowed a simulated window. Your twist is a
*budget calculation*: given a token budget, work out how many WORDS of notes you
can fit alongside a fixed system prompt and 5 turns of chat history.

Fill in every `TODO(n)`. When you are done run:

    python phases/phase0_fundamentals/context_window/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens  # noqa: E402

SYSTEM_PROMPT = (
    "You are Study Buddy, a patient tutor. Answer only from the student's notes."
)
# The 5 previous turns. Each is (user_message, assistant_reply).
HISTORY = [
    ("What is photosynthesis?", "It converts light into chemical energy."),
    ("Where does it happen?", "In the chloroplasts of plant cells."),
    ("What pigment absorbs light?", "Chlorophyll, mostly red and blue light."),
    ("What gas is released?", "Oxygen, from splitting water."),
    ("What is the Calvin cycle?", "The light-independent stage that fixes CO2."),
]
# The model's reply must fit too; reserve this many tokens for it.
REPLY_RESERVE_TOKENS = 400
# Total budget for this one call, input + output.
CONTEXT_BUDGET = 8000
# Approximation used to convert leftover tokens into words.
WORDS_PER_TOKEN = 0.75


def tokens_used_so_far() -> int:
    """Tokens taken by the system prompt plus all 5 history turns.

    TODO(1): sum count_tokens() over the system prompt and every history string
    (both the user message and the assistant reply of each turn). Return the total.
    """
    raise NotImplementedError("TODO(1): total the system prompt and history tokens")


def note_budget_words() -> int:
    """How many WORDS of notes fit in what's left, after reserving the reply.

    TODO(2):
      left  = CONTEXT_BUDGET - REPLY_RESERVE_TOKENS - tokens_used_so_far()
      words = int(left * WORDS_PER_TOKEN)      # floor it
      Return 0 if left < 0 (the fixed stuff alone already overflows).
    """
    raise NotImplementedError("TODO(2): compute the words of notes that fit")


if __name__ == "__main__":
    print("fixed tokens used:", tokens_used_so_far())
    print(f"reply reserve   : {REPLY_RESERVE_TOKENS}")
    print(f"budget          : {CONTEXT_BUDGET}")
    print("note words that fit:", note_budget_words())
