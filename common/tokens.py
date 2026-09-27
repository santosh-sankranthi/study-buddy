"""Token counting helpers shared by the Phase 0 and Phase 2 concepts.

`tiktoken` is OpenAI's reference tokenizer. It is *not* the exact tokenizer the
model behind OpenRouter uses, but it is close enough to build intuition, and it
is deterministic -- which is what you want when teaching.
"""

from __future__ import annotations

import tiktoken

# The two encodings students compare in the Phase 0 "tokens" twist.
# cl100k_base  -> GPT-4 / GPT-3.5 family, ~100k vocabulary
# o200k_base   -> GPT-4o family, larger vocabulary, fewer tokens for many texts
ENCODINGS = ("cl100k_base", "o200k_base")


def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    """Return the number of tokens in ``text`` under the named encoding."""
    enc = tiktoken.get_encoding(encoding)
    return len(enc.encode(text))


def tokens_of_messages(messages: list[dict], encoding: str = "cl100k_base") -> int:
    """Count tokens for a whole chat ``messages`` list.

    Real chat APIs add a few tokens per message for role/formatting overhead
    (commonly ~4 per message plus ~3 to prime the reply). We add that here so the
    context-budget exercise in Phase 0 gives realistic numbers.
    """
    enc = tiktoken.get_encoding(encoding)
    total = 3  # priming tokens for the assistant reply
    for message in messages:
        total += 4  # per-message formatting overhead
        total += len(enc.encode(message.get("content", "")))
        total += len(enc.encode(message.get("role", "")))
    return total
