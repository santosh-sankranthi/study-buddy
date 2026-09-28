"""Study Buddy — the evolving backend.

This file grows every phase. Reading the git diff between two phase tags shows
exactly what changed and why.

Phase progression:
  v0  — raw one-shot Q&A (the starting point)
  v1  — system prompts, CoT, structured output (/modes, /flashcards, /quiz-item, /study-plan, /tools)
  v2  — session memory, context compaction, context report, long-context measurement
  v3  — embeddings + vector database (/embed, /similarity-demo, /semantic-search, /notes/*)
  v4  — grounded RAG in /ask
  v5  — agents (/agent/ask, /agent/plan-and-execute)
  v6  — MCP (/mcp/tools)
  v7  — security middleware (injection, PII, moderation)
  v8  — evaluation endpoints (/eval/groundedness-report, /eval/regression-report)

How to read this file
  Every meaningful block is prefixed with a comment banner:

      # CONCEPT · <name>  [<phase>]
      # <one line on what this block does, and what was broken before it>

  The banners are the lesson map. Read them in order and the file's growth is
  the whole workshop. Helper logic lives in the `app/` modules and is imported,
  not re-written here -- so this file stays about *wiring concepts together*.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Locate the app package by walking up from this file, so this module works
# both as app/main.py and as a snapshot under app/versions/vN/.
_APP_DIR = Path(__file__).resolve()
while _APP_DIR.name != "app" and _APP_DIR.parent != _APP_DIR:
    _APP_DIR = _APP_DIR.parent
sys.path.insert(0, str(_APP_DIR.parent))

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from common.llm import chat
from common.tokens import count_tokens

STATIC_DIR = _APP_DIR / "static"

app = FastAPI(title="Study Buddy", version="v0")

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · /meta — capability manifest  [all phases]
# Report which concepts this version has, so the UI reveals only those controls.
# ────────────────────────────────────────────────────────────────────────────
@app.get("/meta")
def meta() -> dict:
    """What this version supports; the frontend gates its controls on this."""
    return {"version": "v0", "features": []}

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · /ask — the core endpoint  [Phase 0-9]
# One question in, one answer out. Each phase adds one step inside this function.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Raw one-shot forward pass: no persona, no memory, no grounding."""
    raw = chat(
        [{"role": "user", "content": request.question}],
        temperature=0.7,
    )
    return AskResponse(answer=raw)

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Frontend  [all phases]
# Serve the single-page UI; every phase of the workshop is driven through it.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
