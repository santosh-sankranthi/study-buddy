"""SOLUTION -- Context Windows (reference answer to the twist)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens  # noqa: E402

SYSTEM_PROMPT = (
    "You are Study Buddy, a patient tutor. Answer only from the student's notes."
)
HISTORY = [
    ("What is photosynthesis?", "It converts light into chemical energy."),
    ("Where does it happen?", "In the chloroplasts of plant cells."),
    ("What pigment absorbs light?", "Chlorophyll, mostly red and blue light."),
    ("What gas is released?", "Oxygen, from splitting water."),
    ("What is the Calvin cycle?", "The light-independent stage that fixes CO2."),
]
REPLY_RESERVE_TOKENS = 400
CONTEXT_BUDGET = 8000
WORDS_PER_TOKEN = 0.75


def tokens_used_so_far() -> int:
    """Tokens taken by the system prompt plus all 5 history turns."""
    total = count_tokens(SYSTEM_PROMPT)
    for user_message, assistant_reply in HISTORY:
        total += count_tokens(user_message)
        total += count_tokens(assistant_reply)
    return total


def note_budget_words() -> int:
    """How many words of notes fit in what's left, after reserving the reply."""
    left = CONTEXT_BUDGET - REPLY_RESERVE_TOKENS - tokens_used_so_far()
    if left < 0:
        return 0
    return int(left * WORDS_PER_TOKEN)


if __name__ == "__main__":
    print("fixed tokens used:", tokens_used_so_far())
    print(f"reply reserve   : {REPLY_RESERVE_TOKENS}")
    print(f"budget          : {CONTEXT_BUDGET}")
    print("note words that fit:", note_budget_words())
