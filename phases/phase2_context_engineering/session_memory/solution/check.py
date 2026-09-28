"""Self-check -- Session Memory exercise.

Run:
    python phases/phase2_context_engineering/session_memory/solution/check.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

spec = importlib.util.spec_from_file_location(
    "ex", Path(__file__).resolve().parents[1] / "exercise" / "main.py"
)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

print("Checking session memory exercise ...\n")

# Check total history tokens
tot = ex.total_history_tokens(ex.SAMPLE_HISTORY)
assert tot > 200, f"Expected total tokens > 200, got {tot}"
print(f"✅  total_history_tokens calculated correctly ({tot} tokens)")

# Check trimming with small budget
trimmed_small = ex.test_trim(budget=50)
assert len(trimmed_small) == 2, f"Expected exactly 2 most recent messages, got {len(trimmed_small)}"
assert trimmed_small[-1]["content"] == "Augustus Caesar was the first emperor."
assert trimmed_small[0]["content"] == "Who was the first emperor?"
print("✅  trim_to_token_budget keeps most recent messages within budget")

# Check trimming with large budget
trimmed_large = ex.test_trim(budget=10_000)
assert len(trimmed_large) == len(ex.SAMPLE_HISTORY), "Large budget should retain all messages"
print("✅  Large budget retains full conversation history")

print("\n✅  All checks passed!")
