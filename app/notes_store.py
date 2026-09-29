"""Persistent notes store — notes a student saves that survive new sessions.

Phase 3 — backs the ``store_note`` / ``get_note`` / ``list_notes`` agent tools.

Unlike ``app/memory.py`` (session history held in process memory and lost when
the server restarts), these notes are plain Markdown files under ``data/notes/``,
so they persist across new chat sessions and server restarts. That contrast is
the point: "memory" in a prompt is not the same as storage on disk.

Wired into: app/tools.py (agent + MCP tool implementations).
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

#: Where saved notes live. Created on first write; git-ignored (personal data).
NOTES_DIR = Path(__file__).resolve().parent.parent / "data" / "notes"


def slug(topic: str) -> str:
    """Turn a topic into a safe file stem: 'Bio exam!' -> 'bio-exam'."""
    cleaned = re.sub(r"[^a-z0-9]+", "-", topic.strip().lower()).strip("-")
    return cleaned or "note"


def save_note(topic: str, content: str) -> Path:
    """Append *content* under *topic* and return the file path.

    Re-saving the same topic appends a dated bullet instead of overwriting, so
    nothing a student wrote is silently lost.
    """
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    path = NOTES_DIR / f"{slug(topic)}.md"

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    entry = f"- [{stamp}] {content.strip()}"

    if path.exists():
        text = path.read_text(encoding="utf-8").rstrip() + "\n" + entry + "\n"
    else:
        text = f"# {topic.strip()}\n\n{entry}\n"
    path.write_text(text, encoding="utf-8")
    return path


def load_note(topic: str) -> str | None:
    """Return the stored note for *topic*, or None if there isn't one.

    Falls back to a fuzzy filename match so "biology exam" finds
    ``biology-exam.md``.
    """
    if not NOTES_DIR.exists():
        return None
    exact = NOTES_DIR / f"{slug(topic)}.md"
    if exact.exists():
        return exact.read_text(encoding="utf-8")

    wanted = slug(topic)
    for path in sorted(NOTES_DIR.glob("*.md")):
        if wanted in path.stem or path.stem in wanted:
            return path.read_text(encoding="utf-8")
    return None


def list_notes() -> list[dict]:
    """Return [{topic, file, chars}] for every saved note."""
    if not NOTES_DIR.exists():
        return []
    out: list[dict] = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        first = next((ln for ln in text.splitlines() if ln.strip()), "")
        title = first.lstrip("# ").strip() or path.stem
        out.append({"topic": title, "file": path.name, "chars": len(text)})
    return out


def all_notes() -> list[tuple[str, str]]:
    """Return [(topic, full_text)] for every saved note (for searching)."""
    result: list[tuple[str, str]] = []
    for item in list_notes():
        path = NOTES_DIR / item["file"]
        result.append((item["topic"], path.read_text(encoding="utf-8", errors="ignore")))
    return result
