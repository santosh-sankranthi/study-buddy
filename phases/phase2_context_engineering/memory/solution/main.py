"""SOLUTION -- Token-Budget Memory Trimming."""
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
    return sum(count_tokens(m.get("content", "")) for m in history)

def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    kept = []
    total = 0
    for msg in reversed(history):
        toks = count_tokens(msg.get("content", ""))
        if total + toks > budget:
            break
        kept.append(msg)
        total += toks
    return list(reversed(kept))

if __name__ == "__main__":
    print("Total tokens:", total_history_tokens(SAMPLE_HISTORY))
    print("Trimmed:", trim_to_token_budget(SAMPLE_HISTORY, 25))
