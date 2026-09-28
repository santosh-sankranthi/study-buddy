"""Self-check -- Context Compaction exercise.

Run:
    python phases/phase2_context_engineering/context_compaction/solution/check.py
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

print("Checking context compaction exercise ...\n")

from app import memory

sid = "check-compact-keep2"
ex.setup_test_conversation(sid)
assert len(memory.get_history(sid)) == 6, "Expected 6 messages after setup"
print("✅  setup_test_conversation creates 6 messages")

history = ex.run_and_verify_keep_last2(sid)
assert len(history) == 3, f"Expected exactly 3 messages after keep_last2, got {len(history)}"
print("✅  Compacted history contains exactly 3 messages")

assert history[0]["role"] == "system" and "[SUMMARY" in history[0]["content"]
print("✅  First message is a [SUMMARY] system message")

assert history[1]["content"] == "And the third law?"
assert "opposite reaction" in history[2]["content"]
print("✅  Last 2 turns preserved verbatim")

print("\n✅  All checks passed!")
