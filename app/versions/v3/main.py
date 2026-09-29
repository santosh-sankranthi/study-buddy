"""Study Buddy — the evolving backend.

This file grows every phase. Reading the git diff between two phase tags shows
exactly what changed and why.

Phase progression:
  v0  — raw one-shot Q&A (the starting point)
  v1  — system prompts, CoT, structured output (/modes, /flashcards, /quiz-item, /study-plan, /tools)
  v2  — session memory, context compaction, context report, long-context measurement
  v3  — agents (/agent/ask, /agent/plan-and-execute)
  v4  — MCP (/mcp/tools)
  v5  — security middleware (injection, PII, moderation)
  v6  — evaluation endpoint (/eval/regression-report)

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
import re
import time
from pathlib import Path

# Locate the app package by walking up from this file, so this module works
# both as app/main.py and as a snapshot under app/versions/vN/.
_APP_DIR = Path(__file__).resolve()
while _APP_DIR.name != "app" and _APP_DIR.parent != _APP_DIR:
    _APP_DIR = _APP_DIR.parent
sys.path.insert(0, str(_APP_DIR.parent))

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, TypeAdapter

from common.llm import chat
from common.tokens import count_tokens
from app.prompts import build_few_shot_prompt, build_system
from app.schemas import Flashcard, QuizItem, StudyPlanDay
from app.tools import TOOLS
from app.context import context_budget_warning, context_report

STATIC_DIR = _APP_DIR / "static"

app = FastAPI(title="Study Buddy", version="v3")

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · /meta — capability manifest  [all phases]
# Report which concepts this version has, so the UI reveals only those controls.
# ────────────────────────────────────────────────────────────────────────────
@app.get("/meta")
def meta() -> dict:
    """What this version supports; the frontend gates its controls on this."""
    try:
        from common.llm import provider_info
        provider = provider_info()
    except Exception:  # noqa: BLE001
        provider = {}
    return {"version": "v3", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'agents'], **provider}

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · API request / response contract  [Phase 1.4]
# Pydantic types the request we accept and the response we return.
# ────────────────────────────────────────────────────────────────────────────

class AskRequest(BaseModel):
    question:         str
    mode:             str        = "tutor"
    cot:              bool       = False
    temperature:      float      = 0.7
    top_p:            float      = 1.0
    session_id:       str | None = None
    student_name:     str | None = None
    study_goal:       str | None = None
    compact_strategy: str        = "halve"   # "halve" | "keep_last2"


class AskResponse(BaseModel):
    answer:          str
    thinking:        str | None = None
    input_tokens:    int = 0
    output_tokens:   int = 0
    context_report:  dict = {}
    context_warning: str | None = None
    compacted:       bool = False

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · /ask — the core endpoint  [Phase 0-6]
# One question in, one answer out. Each phase adds one step inside this function.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Send a question to Study Buddy. Behaviour grows phase by phase."""

    # ── CONCEPT · Memory [Phase 2.2] ─────────────────────────────────────────
    # Reload earlier turns so the tutor remembers. Compaction shrinks long history.
    compacted = False
    history: list[dict] = []
    if request.session_id:
        from app.memory import (
            append, compact_if_needed, compact_keep_last2, get_history,
        )
        if request.compact_strategy == "keep_last2":
            compacted = compact_keep_last2(request.session_id)
        else:
            compacted = compact_if_needed(request.session_id)
        history = get_history(request.session_id)

    # ── CONCEPT · System prompt [Phase 1.1] ──────────────────────────────────
    # Prepend a `system` message: who the tutor is and the rules it must follow.
    system_content = build_system(
        mode=request.mode,
        student_name=request.student_name,
        study_goal=request.study_goal,
    )

    messages: list[dict] = []
    if system_content:
        messages.append({"role": "system", "content": system_content})
    messages += history

    # ── CONCEPT · Chain of thought [Phase 1.3] ───────────────────────────────
    # Ask the model to reason step by step, tagged so we can split it out later.
    user_content = request.question
    if request.cot:
        user_content += (
            "\n\nThink step by step before answering. "
            "Wrap your reasoning in <thinking>...</thinking> "
            "and your final answer in <answer>...</answer>."
        )
    messages.append({"role": "user", "content": user_content})

    # ── CONCEPT · Context window [Phase 2.1] ─────────────────────────────────
    # Measure the tokens the prompt uses and warn before we hit the model's limit.
    ctx_warning = context_budget_warning(messages)
    ctx_report  = context_report(messages)

    # ── The model call itself (the one thing v0 already did) ─────────────────
    raw_answer = chat(messages, temperature=request.temperature, top_p=request.top_p)

    # ── CONCEPT · Chain of thought — separate reasoning from the answer ──────
    thinking: str | None = None
    final_answer = raw_answer
    if request.cot:
        t_match = re.search(r"<thinking>(.*?)</thinking>", raw_answer, re.DOTALL)
        a_match = re.search(r"<answer>(.*?)</answer>", raw_answer, re.DOTALL)
        if t_match:
            thinking = t_match.group(1).strip()
        if a_match:
            final_answer = a_match.group(1).strip()

    # ── CONCEPT · Memory — store this turn so the next one remembers it ──────
    if request.session_id:
        append(request.session_id, "user", request.question)
        append(request.session_id, "assistant", final_answer)

    input_tokens = count_tokens(" ".join(m.get("content") or "" for m in messages))
    return AskResponse(
        answer=final_answer,
        thinking=thinking,
        input_tokens=input_tokens,
        output_tokens=count_tokens(final_answer),
        context_report=ctx_report,
        context_warning=ctx_warning,
        compacted=compacted,
    )

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Personas / modes  [Phase 1.1]
# List the tutor personas the frontend can choose from.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/modes")
def list_modes() -> list[str]:
    return ["tutor", "direct", "flashcard"]

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Few-shot  [Phase 1.2]
# Two worked Q&A -> MCQ examples fix the JSON shape of /quiz-item.
# ────────────────────────────────────────────────────────────────────────────

QUIZ_EXAMPLES = [
    {
        "input":  "Photosynthesis",
        "output": (
            '{"question": "Where does photosynthesis occur?", '
            '"options": ["Mitochondria", "Chloroplast", "Nucleus", "Ribosome"], '
            '"correct_index": 1}'
        ),
    },
    {
        "input":  "Newton\'s first law",
        "output": (
            '{"question": "What does Newton\'s first law state?", '
            '"options": ["F = ma", "Objects in motion stay in motion unless acted on", '
            '"Every action has an equal reaction", "Gravity attracts masses"], '
            '"correct_index": 1}'
        ),
    },
]


@app.post("/quiz-item")
def make_quiz_item(body: dict) -> dict:
    topic    = body.get("topic", "")
    messages = [
        {"role": "system", "content": "Return ONLY a valid JSON object matching the QuizItem schema. No other text."},
    ] + build_few_shot_prompt(QUIZ_EXAMPLES, topic)
    raw  = chat(messages, temperature=0.3)
    item = QuizItem.model_validate_json(raw)

    session_id = body.get("session_id")
    if session_id:
        from app.memory import add_quiz_item
        add_quiz_item(session_id, item.model_dump())

    return item.model_dump()

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Structured output  [Phase 1.4]
# Pydantic validates the model's JSON, or raises ValidationError.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/flashcards")
def make_flashcards(body: dict) -> dict:
    topic = body.get("topic", "")
    messages = [
        {
            "role":    "system",
            "content": (
                'Return a valid JSON object: {"question":"...","answer":"...","difficulty":"easy|medium|hard"}. '
                "No other text, no markdown fences."
            ),
        },
        {"role": "user", "content": f"Topic: {topic}"},
    ]
    raw  = chat(messages, temperature=0.3)
    card = Flashcard.model_validate_json(raw)
    return card.model_dump()

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Structured output (a list)  [Phase 1.4]
# A multi-day plan validated against StudyPlanDay and a time budget.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/study-plan")
def make_study_plan(body: dict) -> list:
    subjects    = body.get("subjects", [])
    total_hours = body.get("total_hours", 4)
    messages = [
        {
            "role":    "system",
            "content": (
                "Return a valid JSON array of StudyPlanDay objects. "
                'Each object: {"subject":"...","topics":["..."],"minutes":<int>}. '
                f"Total minutes must not exceed {total_hours * 60}. "
                "No other text, no markdown fences."
            ),
        },
        {
            "role":    "user",
            "content": f"Subjects: {', '.join(subjects)}. Total hours available: {total_hours}.",
        },
    ]
    raw  = chat(messages, temperature=0.3)
    ta   = TypeAdapter(list[StudyPlanDay])
    plan = ta.validate_json(raw)
    total_mins = sum(d.minutes for d in plan)
    if total_mins > total_hours * 60:
        raise HTTPException(
            status_code=422,
            detail=f"Study plan exceeds the time budget: {total_mins} > {total_hours * 60} minutes.",
        )
    return [d.model_dump() for d in plan]

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Function calling (schemas)  [Phase 1.5]
# Publish the JSON tool contracts; nothing is executed yet.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/tools")
def list_tools() -> list:
    return TOOLS

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Context sources  [Phase 2.1]
# Show where the prompt's tokens go, broken down by role.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/context-report")
def get_context_report(session_id: str | None = None) -> dict:
    messages: list[dict] = []
    if session_id:
        from app.memory import get_history
        messages = get_history(session_id)
    return context_report(messages)

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Memory (API)  [Phase 2.2]
# Read or clear a session's stored conversation.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/session/{session_id}/history")
def get_session_history(session_id: str) -> list:
    from app.memory import get_history
    return get_history(session_id)


@app.delete("/session/{session_id}")
def clear_session(session_id: str) -> dict:
    from app.memory import clear
    clear(session_id)
    return {"cleared": True, "session_id": session_id}

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Long context  [Phase 2.4]
# Measure latency and cost as the pasted document grows.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/measure-long-context")
def measure_long_context(body: dict) -> list:
    """Measure latency and cost as document token count grows in steps."""
    import tiktoken
    doc_text = body.get("text", "")
    question = "Summarise the above in one sentence."
    enc      = tiktoken.get_encoding("cl100k_base")
    results  = []

    PRICE_PER_M_TOKENS = 0.50  # approximate — adjust to the model's real price

    for tokens_target in [500, 1_000, 2_000, 4_000]:
        ids   = enc.encode(doc_text)[:tokens_target]
        text  = enc.decode(ids)
        msgs  = [{"role": "user", "content": text + "\n\n" + question}]

        t0      = time.monotonic()
        _       = chat(msgs, temperature=0.0)
        latency = round((time.monotonic() - t0) * 1_000)

        actual_tokens = len(ids)
        results.append({
            "target_tokens": tokens_target,
            "actual_tokens": actual_tokens,
            "latency_ms":    latency,
            "est_cost_usd":  round(actual_tokens / 1_000_000 * PRICE_PER_M_TOKENS, 6),
        })
    return results

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Agents  [Phase 3]
# A ReAct loop that calls tools, plus a planner->executor->critic pipeline.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/agent/ask")
def agent_ask(body: dict) -> dict:
    from app.agent import agent_loop
    return agent_loop(body.get("question", ""))


@app.post("/agent/plan-and-execute")
def agent_plan_and_execute(body: dict) -> dict:
    from app.agent import plan_and_execute
    return plan_and_execute(body.get("question", ""))

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Frontend  [all phases]
# Serve the single-page UI; every phase of the workshop is driven through it.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
