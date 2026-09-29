"""EXERCISE -- Context Compaction.

Practice: compress a long chat by replacing old turns with one summary message.

Task: finish compact_keep_last2() so it keeps a summary plus the last two turns.

Check your work with:
    python phases/phase2_context_engineering/context_compaction/solution/check.py
"""

CONVERSATION = [
    {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i}"}
    for i in range(8)
]


def compact_keep_last2(messages: list[dict]) -> list[dict]:
    """Return a system summary followed by the last two messages."""
    # TODO: if there are more than 4 messages, return
    #   [{"role": "system", "content": "[SUMMARY] ..."}] + messages[-2:]
    # otherwise return messages unchanged.
    raise NotImplementedError("compact_keep_last2")


if __name__ == "__main__":
    print("Compacted:", compact_keep_last2(CONVERSATION))
