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

class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Raw one-shot forward pass: no persona, no memory, no grounding."""
    raw = chat(
        [{"role": "user", "content": request.question}],
        temperature=0.7,
    )
    return AskResponse(answer=raw)

@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
