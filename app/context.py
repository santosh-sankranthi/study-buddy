"""Context utilities — building and analysing the prompt context.

Grows through the phases:
  Phase 2.1 — context_report(), context_budget_warning()
"""

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Context window  [Phase 2.1]
# The context window is a hard token budget (input + output). This module counts
# where the prompt's tokens go and warns before we reach the limit.
# Wired into: /ask (context_report, context_budget_warning), /context-report.
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from common.tokens import count_tokens

MODEL_LIMIT = 8_000   # conservative token budget for free-tier models


# ── Phase 2.1 ────────────────────────────────────────────────────────────────

def context_report(messages: list[dict]) -> dict:
    """Return a per-role token breakdown for the given messages list.

    Keys: "system", "user", "assistant", "tool", "total".
    """
    report: dict[str, int] = {"system": 0, "user": 0, "assistant": 0, "tool": 0}
    for m in messages:
        role = m.get("role", "other")
        key  = role if role in report else "user"
        report[key] += count_tokens(m.get("content", "") or "")
    report["total"] = sum(report.values())
    return report


def context_budget_warning(messages: list[dict], limit: int = MODEL_LIMIT) -> str | None:
    """Return a warning string when the context is close to the limit, else None.

    Triggers at 80 % of the limit so the instructor can show the banner before
    the call actually fails.
    """
    total = context_report(messages)["total"]
    if total > limit * 0.8:
        return f"⚠️  Approaching context limit ({total:,} / {limit:,} tokens)"
    return None
