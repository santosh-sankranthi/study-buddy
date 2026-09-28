"""Study Buddy v2 — Multi-turn sessions, context budget, compaction, light sanitizer."""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from common.llm import chat
from common.tokens import count_tokens
from app.prompts import build_system
from app.memory import append, clear, compact_if_needed, get_history
from app.context import context_budget_warning, context_report
from app.security import sanitize_input

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
app = FastAPI(title="Study Buddy v2")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class AskRequest(BaseModel):
    question: str
    mode: str = "tutor"
    cot: bool = False
    temperature: float = 0.7
    top_p: float = 1.0
    session_id: str | None = None
    student_name: str | None = None

class AskResponse(BaseModel):
    answer: str
    thinking: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    context_report: dict = {}
    context_warning: str | None = None
    compacted: bool = False

@app.get("/")
def read_root():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    q, flagged = sanitize_input(req.question)
    compacted = False
    if req.session_id:
        compacted = compact_if_needed(req.session_id)

    sys_prompt = build_system(mode=req.mode, student_name=req.student_name, inject_date=True)
    messages = [{"role": "system", "content": sys_prompt}]
    if req.session_id:
        messages += get_history(req.session_id)
    messages.append({"role": "user", "content": q})

    ctx_rep = context_report(messages)
    ctx_warn = context_budget_warning(ctx_rep.get("total", 0))

    raw = chat(messages, temperature=req.temperature, top_p=req.top_p)
    if req.session_id:
        append(req.session_id, "user", q)
        append(req.session_id, "assistant", raw)

    return AskResponse(
        answer=raw,
        input_tokens=count_tokens(q),
        output_tokens=count_tokens(raw),
        context_report=ctx_rep,
        context_warning=ctx_warn,
        compacted=compacted,
    )
