"""Tool schemas and implementations.

Grows through the phases:
  Phase 1.5 — TOOLS list (schemas only, no execution)
  Phase 6.1 — Real Python implementations + TOOL_REGISTRY

Notes tools (store_note / get_note / list_notes) persist to ``data/notes/``
via ``app/notes_store.py`` so saved notes survive new sessions.
"""

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Function calling & tools  [Phase 1.5 schemas / Phase 3 execution]
# The JSON schemas tell the model what it may call; TOOL_REGISTRY maps those
# names to real Python functions that the agent loop actually executes.
# Wired into: /tools (list schemas), /agent/ask (execute), mcp_server/ (expose via MCP).
# ──────────────────────────────────────────────────────────────────────────────

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
    {
        "type": "function",
        "function": {
            "name":        "store_note",
            "description": (
                "Save a note for the student so it can be recalled later — even in a "
                "new session or after a restart. Call this whenever the student asks "
                "you to remember, save, note down, or keep track of something."
            ),
            "parameters": {
                "type":       "object",
                "properties": {
                    "topic": {
                        "type":        "string",
                        "description": "A short title for the note, e.g. 'Biology exam'. Used to find it later.",
                    },
                    "content": {
                        "type":        "string",
                        "description": "The information to remember (facts, dates, definitions, lists).",
                    },
                },
                "required": ["topic", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name":        "get_note",
            "description": "Retrieve a note the student saved earlier, by its topic.",
            "parameters": {
                "type":       "object",
                "properties": {
                    "topic": {
                        "type":        "string",
                        "description": "The topic/title of the saved note to read back.",
                    },
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name":        "list_notes",
            "description": "List all notes the student has saved so far.",
            "parameters": {
                "type":       "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


# ── Phase 6.1: Real implementations ──────────────────────────────────────────
# (These are no-ops until Phase 6; importing this file in Phase 1–5 is safe.)

def search_notes(query: str) -> str:
    """Search the study notes by simple keyword match.

    Looks in two places, in order: notes the student saved with ``store_note``
    (persisted on disk), then the bundled sample course notes. Deliberately
    boring: return notes whose text contains any keyword from the query. No
    embeddings, no database -- so the agent's tool stays obvious and explainable.
    """
    import re
    from pathlib import Path

    words = [w for w in re.findall(r"\w+", query.lower()) if len(w) > 2]
    if not words:
        return "No relevant notes found for that query."

    hits: list[str] = []

    # 1) Notes the student saved themselves (persist across sessions).
    from app.notes_store import all_notes

    for title, text in all_notes():
        if any(w in text.lower() for w in words):
            snippet = text.strip().replace("\n", " ")[:300]
            hits.append(f"[saved note: {title}] {snippet}")
        if len(hits) >= 3:
            return "\n\n".join(hits)

    # 2) The bundled sample course notes.
    notes_dir = Path(__file__).resolve().parent.parent / "data" / "sample_notes"
    if notes_dir.exists():
        for path in sorted(notes_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if any(w in text.lower() for w in words):
                snippet = text.strip().replace("\n", " ")[:300]
                hits.append(f"[{path.name}] {snippet}")
            if len(hits) >= 3:
                break

    return "\n\n".join(hits) if hits else "No relevant notes found for that query."


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


def store_note(topic: str, content: str) -> str:
    """Save a note to disk so it survives new sessions and restarts."""
    from app.notes_store import save_note

    path = save_note(topic, content)
    return f"Saved note {topic!r} to {path.name}. It will be available in future sessions."


def get_note(topic: str) -> str:
    """Read a previously saved note back by topic."""
    from app.notes_store import load_note

    text = load_note(topic)
    if text is None:
        return f"No saved note found for {topic!r}."
    return text


def list_notes() -> str:
    """List the topics of every saved note."""
    from app.notes_store import list_notes as _saved

    items = _saved()
    if not items:
        return "No notes saved yet."
    lines = [f"- {i['topic']}  ({i['file']})" for i in items]
    return "Saved notes:\n" + "\n".join(lines)


#: The dispatcher used by the agent loop (Phase 6+).
TOOL_REGISTRY: dict[str, callable] = {
    "search_notes":      search_notes,
    "get_exam_schedule": get_exam_schedule,
    "calculate_grade":   calculate_grade,
    "store_note":        store_note,
    "get_note":          get_note,
    "list_notes":        list_notes,
}
