"""EXERCISE -- Token-Budget Sliding-Window Memory Trimming.

The demo appended and retrieved full history turns.
Your twist: implement and verify trim_to_token_budget() in app.memory, ensuring
that when a session's history exceeds a token budget, only the most RECENT
messages that fit within the budget are retained.

Fill in every TODO. Run when done:
    python phases/phase2_context_engineering/session_memory/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.memory import trim_to_token_budget
from common.tokens import count_tokens

# Sample conversation history with varying lengths
SAMPLE_HISTORY = [
    {"role": "user", "content": "Tell me about the Roman Empire. " * 30},        # ~200 tokens
    {"role": "assistant", "content": "The Roman Empire was vast. " * 30},       # ~200 tokens
    {"role": "user", "content": "Who was the first emperor?"},                   # ~6 tokens
    {"role": "assistant", "content": "Augustus Caesar was the first emperor."},   # ~8 tokens
]


# ── TODO(1): Compute total tokens in full sample history ─────────────────────
def total_history_tokens(history: list[dict]) -> int:
    """Return the total token count across all messages in history."""
    # TODO(1): sum count_tokens(m['content']) for m in history
    return sum(count_tokens(m["content"]) for m in history)


# ── TODO(2): Test trimming to budget ─────────────────────────────────────────
def test_trim(budget: int = 50) -> list[dict]:
    """Trim SAMPLE_HISTORY to fit within `budget` tokens."""
    # TODO(2): call trim_to_token_budget(SAMPLE_HISTORY, budget)
    return trim_to_token_budget(SAMPLE_HISTORY, budget)


if __name__ == "__main__":
    tot = total_history_tokens(SAMPLE_HISTORY)
    print(f"Total tokens in untrimmed history: {tot}")
    trimmed = test_trim(50)
    print(f"Trimmed to budget 50 tokens (retained {len(trimmed)} of {len(SAMPLE_HISTORY)} messages):")
    for m in trimmed:
        print(f"  {m['role']}: {m['content']}")
