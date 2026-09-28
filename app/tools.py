"""Tool schemas and implementations.

Grows through the phases:
  Phase 1.5 — TOOLS list (schemas only, no execution)
  Phase 6.1 — Real Python implementations + TOOL_REGISTRY
"""

from __future__ import annotations

# ── Phase 1.5: Tool schemas (JSON Schema format for OpenAI tool-calling API) ──

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name":        "search_notes",
            "description": "Search the student's notes for content relevant to a query.",
            "parameters": {
                "type":       "object",
                "properties": {
                    "query": {
                        "type":        "string",
                        "description": "The search query — what topic or question to look up.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name":        "get_exam_schedule",
            "description": "Look up when the exam is scheduled for a given subject.",
            "parameters": {
                "type":       "object",
                "properties": {
                    "subject": {
                        "type":        "string",
                        "description": "The subject name (e.g. 'Math', 'Biology').",
                    },
                },
                "required": ["subject"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name":        "calculate_grade",
            "description": "Calculate the weighted average grade from a list of scores and weights.",
            "parameters": {
                "type":       "object",
                "properties": {
                    "scores": {
                        "type":        "array",
                        "items":       {"type": "number"},
                        "description": "List of numeric scores (0–100).",
                    },
                    "weights": {
                        "type":        "array",
                        "items":       {"type": "number"},
                        "description": "List of weights that correspond to each score (fractions, must sum ≤ 1).",
                    },
                },
                "required": ["scores", "weights"],
            },
        },
    },
]


# ── Phase 6.1: Real implementations ──────────────────────────────────────────
# (These are no-ops until Phase 6; importing this file in Phase 1–5 is safe.)

def search_notes(query: str) -> str:
    """Search the student's indexed notes via vector similarity.

    Phase 6 wires this to app.vector_store.retrieve(). Before that, returns
    a placeholder so the tool can be listed without crashing.
    """
    try:
        from app.vector_store import retrieve
        results = retrieve(query, k=2)
        if not results:
            return "No relevant notes found for that query."
        return "\n\n".join(r["text"] for r in results)
    except ImportError:
        return f"[search_notes not yet wired — Phase 4+ needed] query={query!r}"


def get_exam_schedule(subject: str) -> str:
    """Return the hardcoded exam date for a subject."""
    schedule: dict[str, str] = {
        "math":         "2026-11-01",
        "biology":      "2026-11-15",
        "chemistry":    "2026-11-22",
        "physics":      "2026-12-01",
        "history":      "2026-11-08",
        "english":      "2026-11-29",
        "algorithms":   "2026-11-01",
    }
    date = schedule.get(subject.strip().lower())
    if date:
        return f"{subject.capitalize()} exam is scheduled for {date}."
    return f"No exam date found for subject: {subject!r}. Known subjects: {list(schedule.keys())}"


def calculate_grade(scores: list[float], weights: list[float]) -> str:
    """Return the weighted average grade."""
    if len(scores) != len(weights):
        return "Error: scores and weights must have the same number of entries."
    if not scores:
        return "Error: scores list is empty."
    total_weight = sum(weights)
    if total_weight == 0:
        return "Error: weights must not all be zero."
    grade = sum(s * w for s, w in zip(scores, weights)) / total_weight
    return f"Weighted average grade: {grade:.2f}%"


#: The dispatcher used by the agent loop (Phase 6+).
TOOL_REGISTRY: dict[str, callable] = {
    "search_notes":      search_notes,
    "get_exam_schedule": get_exam_schedule,
    "calculate_grade":   calculate_grade,
}
