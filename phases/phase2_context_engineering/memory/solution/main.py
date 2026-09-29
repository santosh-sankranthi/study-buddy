"""SOLUTION -- Token-Budget Memory.

Reference answer: count each message and keep the newest ones that fit.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

SAMPLE_HISTORY = [
    {"role": "user", "content": "What is ATP?"},
    {"role": "assistant", "content": "ATP is the primary energy currency of cells."},
    {"role": "user", "content": "How is it produced?"},
    {"role": "assistant", "content": "It is produced during cellular respiration in mitochondria."},
]


def total_history_tokens(history: list[dict]) -> int:
    """Return the total tokens across every message's content."""
    return sum(count_tokens(m.get("content", "")) for m in history)


def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    """Return the newest messages whose tokens fit within `budget`."""
    kept: list[dict] = []
    used = 0
    for message in reversed(history):
        cost = count_tokens(message.get("content", ""))
        if used + cost > budget:
            break
        kept.append(message)
        used += cost
    return list(reversed(kept))


if __name__ == "__main__":
    print("Total tokens:", total_history_tokens(SAMPLE_HISTORY))
    print("Trimmed:", trim_to_token_budget(SAMPLE_HISTORY, 20))
