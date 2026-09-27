"""Study Buddy -- v0: deliberately unimpressive.

This is the *starting point* of the whole workshop. It is a single-file FastAPI
backend whose only job is: take a question, send it raw to the LLM, return the
answer. There is:

  * no system prompt  -> generic, inconsistent answers
  * no history        -> it forgets every previous turn
  * no memory/notes   -> it cannot ground answers in the student's material
  * no tools/agents   -> it cannot do anything requiring more than one step

Every later phase exists to fix one visible limitation of this file. That is
why it is written to be as plain as possible -- the contrast is the lesson.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the repo-root `common` package importable when running `uvicorn app.main:app`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from common.llm import chat  # noqa: E402

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Study Buddy", version="v0")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Send the question raw to the model. One message in, one message out."""
    # The whole "context" is a single user message. Nothing else.
    answer = chat([{"role": "user", "content": request.question}])
    return AskResponse(answer=answer)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
