"""SOLUTION -- Context Compaction.

Reference answer: replace everything but the last two turns with a summary.
"""

CONVERSATION = [
    {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"}
    for i in range(8)
]


def compact_keep_last2(messages: list[dict]) -> list[dict]:
    """Return a system summary followed by the last two messages."""
    if len(messages) <= 4:
        return messages
    summary = {"role": "system", "content": f"[SUMMARY] {len(messages) - 2} earlier messages"}
    return [summary] + messages[-2:]


if __name__ == "__main__":
    print("Compacted:", compact_keep_last2(CONVERSATION))
