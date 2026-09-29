"""EXERCISE -- Token-Budget Memory.

Practice: keep a chat history under a token budget by dropping old messages.

Task: finish total_history_tokens() and trim_to_token_budget().

Check your work with:
    python phases/phase2_context_engineering/memory/solution/check.py
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
    raise NotImplementedError("total_history_tokens")


def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    """Return the newest messages whose tokens fit within `budget`."""
    raise NotImplementedError("trim_to_token_budget")


if __name__ == "__main__":
    print("Total tokens:", total_history_tokens(SAMPLE_HISTORY))
