"""EXERCISE -- Keep-Last-2 Context Compaction Strategy.

The demo compacted history by halving it.
Your twist: implement and test compact_keep_last2(session_id) in app.memory,
which summarizes all history except the most recent 2 messages, resulting in
exactly: [SUMMARY system message] + last 2 messages verbatim.

Fill in every TODO. Run when done:
    python phases/phase2_context_engineering/context_compaction/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app import memory

TEST_SESSION = "exercise-compact-test"


# ── TODO(1): Populate test session with 6 messages ───────────────────────────
def setup_test_conversation(session_id: str) -> None:
    """Clear session and populate with 6 messages (3 user/assistant pairs)."""
    memory.clear(session_id)
    # TODO(1): append 3 pairs of messages (user / assistant)
    memory.append(session_id, "user", "What is Newton's first law?")
    memory.append(session_id, "assistant", "An object remains at rest or in uniform motion unless acted upon by a net force.")
    memory.append(session_id, "user", "What about Newton's second law?")
    memory.append(session_id, "assistant", "Force equals mass times acceleration (F = ma).")
    memory.append(session_id, "user", "And the third law?")
    memory.append(session_id, "assistant", "For every action, there is an equal and opposite reaction.")


# ── TODO(2): Run compact_keep_last2 and verify resulting history ──────────────
def run_and_verify_keep_last2(session_id: str) -> list[dict]:
    """Run compact_keep_last2 on session and return the resulting history."""
    # TODO(2): call memory.compact_keep_last2(session_id) and return memory.get_history(session_id)
    success = memory.compact_keep_last2(session_id)
    assert success is True, "Expected compaction to return True"
    return memory.get_history(session_id)


if __name__ == "__main__":
    setup_test_conversation(TEST_SESSION)
    before = memory.get_history(TEST_SESSION)
    print(f"Setup conversation: {len(before)} messages.")

    after = run_and_verify_keep_last2(TEST_SESSION)
    print(f"After compact_keep_last2: {len(after)} messages.")
    for i, m in enumerate(after, 1):
        print(f"  [{i}] {m['role']}: {m['content'][:60]}...")
