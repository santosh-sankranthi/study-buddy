"""EXERCISE -- Token-Budget Memory Trimming.

The demo kept the last N turns.
Your twist: implement total_history_tokens() and trim_to_token_budget()
to trim messages based on token limits rather than turn counts.

Run when done:
    python phases/phase2_context_engineering/memory/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

SAMPLE_HISTORY = [
    {"role": "user", "content": "What is ATP?"},
    {"role": "assistant", "content": "ATP is the primary energy currency of cells."},
    {"role": "user", "content": "How is it produced?"},
    {"role": "assistant", "content": "It is produced during cellular respiration in mitochondria."},
]

# TODO(1): Implement total_history_tokens(history: list[dict]) -> int
def total_history_tokens(history: list[dict]) -> int:
    raise NotImplementedError("TODO(1): implement total_history_tokens")

# TODO(2): Implement trim_to_token_budget(history: list[dict], budget: int) -> list[dict]
def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    raise NotImplementedError("TODO(2): implement trim_to_token_budget")

if __name__ == "__main__":
    print("Total tokens:", total_history_tokens(SAMPLE_HISTORY))
