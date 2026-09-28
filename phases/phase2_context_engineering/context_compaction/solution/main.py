"""SOLUTION -- Context Compaction: Keep Last 2."""
def setup_test_conversation(session_id: str) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i} in session {session_id}"}
        for i in range(8)
    ]

def compact_keep_last2(messages: list[dict]) -> list[dict]:
    if len(messages) <= 4:
        return messages
    older = messages[:-2]
    last2 = messages[-2:]
    summary = f"[SUMMARY] Conversation covered {len(older)} earlier turns."
    return [{"role": "system", "content": summary}] + last2

if __name__ == "__main__":
    conv = setup_test_conversation("session_1")
    print("Compacted:", compact_keep_last2(conv))
