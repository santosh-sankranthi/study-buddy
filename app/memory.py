"""Session memory — conversation history management.

Grows through the phases:
  Phase 2.2 — SessionStore, get_history(), append(), clear()
  Phase 2.2 — trim_to_token_budget()
  Phase 2.3 — summarize(), compact_if_needed(), compact_keep_last2()
  Phase 2.3 — compact() — the on-demand /compact command, with a before/after report
"""

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Memory & context compaction  [Phase 2.2-2.3]
# The model is stateless, so "memory" is just history we re-send. This module
# stores it per session, trims it to a token budget, and summarises the oldest
# half when it grows too long (compaction).
# Wired into: /ask, the /session/{id} endpoints, and /session/{id}/compact
# (the /compact chat command).
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from collections import defaultdict

from common.tokens import count_tokens

# ── Storage ───────────────────────────────────────────────────────────────────

#: In-memory store: session_id → list of chat messages (non-system only).
_store: dict[str, list[dict]] = defaultdict(list)

#: Quiz history: session_id → list of quiz items shown.
_quiz_history: dict[str, list[dict]] = defaultdict(list)

COMPACT_BUDGET = 6_000   # tokens — trigger compaction above this


# ── Basic operations ──────────────────────────────────────────────────────────

def get_history(session_id: str) -> list[dict]:
    """Return the full message history for a session (may be empty list)."""
    return list(_store[session_id])   # defensive copy


def append(session_id: str, role: str, content: str) -> None:
    """Append one message to a session's history."""
    _store[session_id].append({"role": role, "content": content})


def clear(session_id: str) -> None:
    """Wipe all history for a session."""
    _store[session_id] = []


def all_sessions() -> list[str]:
    """List all session IDs that have at least one message."""
    return [sid for sid, msgs in _store.items() if msgs]


# ── Phase 2.2: Token-budget trimming ─────────────────────────────────────────

def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    """Keep as many RECENT messages as fit within *budget* tokens.

    Iterates from the end of history, accumulating messages until the next
    one would exceed the budget, then returns only the kept tail.

    This is harder than last-N-turns trimming and motivates compaction.
    """
    kept: list[dict] = []
    used = 0
    for msg in reversed(history):
        cost = count_tokens(msg.get("content", "")) + 4  # per-message overhead
        if used + cost > budget:
            break
        kept.append(msg)
        used += cost
    return list(reversed(kept))


# ── Phase 2.3: Context compaction ────────────────────────────────────────────

def _total_tokens(messages: list[dict]) -> int:
    return sum(count_tokens(m.get("content", "")) for m in messages)


def summarize(messages: list[dict]) -> str:
    """Call the LLM to produce a 3-sentence summary of *messages*."""
    from common.llm import chat  # late import to avoid circular dependency at module load

    transcript = "\n".join(
        f"{m['role'].upper()}: {m.get('content', '')}" for m in messages
    )
    summary_prompt = [
        {
            "role":    "system",
            "content": (
                "Summarize the following conversation concisely in 3 sentences. "
                "Preserve all key facts the student shared."
            ),
        },
        {"role": "user", "content": transcript},
    ]
    try:
        return chat(summary_prompt, temperature=0.0)
    except Exception:
        # Fallback when running offline / tests without API key
        topics = [m.get("content", "")[:30] for m in messages if m.get("role") == "user"]
        return f"Conversation covered earlier topics: {', '.join(topics)}."


def compact_if_needed(session_id: str, budget: int = COMPACT_BUDGET,
                      force: bool = False) -> bool:
    """Summarize the oldest half of history when over *budget*.

    With ``force=True`` the budget check is skipped, so an explicit request
    (the ``/compact`` command) can shrink a short conversation on demand.
    Returns True if compaction occurred, False otherwise.
    """
    history = _store[session_id]
    if not force and _total_tokens(history) <= budget:
        return False
    if len(history) < 2:
        return False  # nothing worth summarising
    half      = len(history) // 2
    old, new  = history[:half], history[half:]
    summary   = summarize(old)
    _store[session_id] = [
        {"role": "system", "content": f"[SUMMARY OF EARLIER CONVERSATION]\n{summary}"}
    ] + new
    return True


def compact_keep_last2(session_id: str, force: bool = False) -> bool:
    """Alternative compaction: system + summary of all-except-last-2 + last 2 turns.

    Phase 2.3 exercise twist — keeps exactly the most recent 2 messages verbatim.
    With ``force=True`` it compacts a short conversation too (used by the
    ``/compact keep_last2`` command). Returns True if compaction occurred.
    """
    history = _store[session_id]
    if not force and len(history) <= 4:
        return False  # not enough to compact
    if len(history) <= 2:
        return False  # nothing to summarise
    to_summarize = history[:-2]
    last2        = history[-2:]
    summary      = summarize(to_summarize)
    _store[session_id] = [
        {"role": "system", "content": f"[SUMMARY OF EARLIER CONVERSATION]\n{summary}"}
    ] + last2
    return True


def compact(session_id: str, strategy: str = "halve", force: bool = False) -> dict:
    """Compact a session on demand and return a before/after report.

    This is what the ``/compact`` chat command calls: it summarises the stored
    history, then reports how many tokens and messages were saved — the visible
    payoff students see in the UI.
    """
    before        = list(_store[session_id])
    before_tokens = _total_tokens(before)

    if strategy == "keep_last2":
        changed = compact_keep_last2(session_id, force=force)
    else:
        changed = compact_if_needed(session_id, force=force)

    after        = _store[session_id]
    after_tokens = _total_tokens(after)

    # Compaction must actually save tokens. A 3-sentence summary of a very short
    # conversation can be *longer* than the conversation itself, so undo it —
    # reporting an increase would be worse than reporting "already small".
    if changed and after_tokens >= before_tokens:
        _store[session_id] = before
        after        = before
        after_tokens = before_tokens
        changed      = False

    summary = ""
    if changed and after and after[0].get("role") == "system":
        summary = after[0].get("content", "")

    return {
        "compacted":       changed,
        "strategy":        strategy,
        "forced":          force,
        "before_messages": len(before),
        "after_messages":  len(after),
        "before_tokens":   before_tokens,
        "after_tokens":    after_tokens,
        "saved_tokens":    max(before_tokens - after_tokens, 0),
        "summary":         summary,
    }


# ── Quiz history ──────────────────────────────────────────────────────────────

def add_quiz_item(session_id: str, quiz_item: dict) -> None:
    _quiz_history[session_id].append(quiz_item)


def get_quiz_history(session_id: str) -> list[dict]:
    return list(_quiz_history[session_id])
