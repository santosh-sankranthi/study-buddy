"""EXERCISE -- Context Compaction: Keep Last 2.

The demo summarized the oldest half.
Your twist: implement compact_keep_last2() to preserve the running summary
plus only the last 2 turns verbatim.

Run when done:
    python phases/phase2_context_engineering/context_compaction/solution/check.py
"""
def setup_test_conversation(session_id: str) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i} in session {session_id}"}
        for i in range(8)
    ]

# TODO(1): Implement compact_keep_last2(messages: list[dict]) -> list[dict]
def compact_keep_last2(messages: list[dict]) -> list[dict]:
    raise NotImplementedError("TODO(1): implement compact_keep_last2")

if __name__ == "__main__":
    conv = setup_test_conversation("session_1")
    print("Compacted:", compact_keep_last2(conv))
