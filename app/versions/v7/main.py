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
import re
import time
import urllib.request
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
from app.security import moderate, sanitize_input, scrub_pii

STATIC_DIR = _APP_DIR / "static"

app = FastAPI(title="Study Buddy", version="v7")

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
    enable_rag:       bool       = True      # Phase 4+
    enable_security:  bool       = True      # Phase 7+


class AskResponse(BaseModel):
    answer:             str
    thinking:           str | None = None
    grounded:           bool = False
    sources:            list[str] = []
    input_tokens:       int = 0
    output_tokens:      int = 0
    context_report:     dict = {}
    context_warning:    str | None = None
    injection_detected: bool = False
    pii_detected:       bool = False
    pii_types:          list[str] = []
    compacted:          bool = False

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · /ask — the core endpoint  [Phase 0-9]
# One question in, one answer out. Each phase adds one step inside this function.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Send a question to Study Buddy. Behaviour grows phase by phase."""

    # ── CONCEPT · Prompt injection + PII [Phase 8] ───────────────────────────
    # Strip injected instructions and redact personal data before anything runs.
    question           = request.question
    injection_detected = False
    pii_detected       = False
    pii_types: list[str] = []

    if request.enable_security:
        question, injection_detected = sanitize_input(question)
        question, pii_types          = scrub_pii(question)
        pii_detected                 = bool(pii_types)

        input_mod = moderate(question)
        if input_mod.get("flagged"):
            raise HTTPException(
                status_code=422,
                detail=f"Request blocked by content policy. Categories: {input_mod.get('categories', {})}",
            )

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

    # ── CONCEPT · Retrieval [Phase 5] ────────────────────────────────────────
    # Semantic-search the notes for the most relevant chunks; None = nothing close.
    grounded = False
    sources: list[str] = []
    rag_chunks: list[dict] = []
    if request.enable_rag:
        try:
            from app.vector_store import retrieve
            from app.rag import extract_sources
            chunks = retrieve(question, k=3)
            if chunks:
                rag_chunks = chunks
                sources    = extract_sources(chunks)
                grounded   = True
        except Exception:  # noqa: BLE001 — RAG not set up yet is fine
            pass

    # ── CONCEPT · Grounded generation [Phase 5] ──────────────────────────────
    # If we retrieved notes, build a prompt that answers ONLY from those chunks.
    if grounded and rag_chunks:
        from app.rag import build_rag_prompt
        messages = build_rag_prompt(question, rag_chunks)
        # Prepend history before the RAG user message.
        if history:
            messages = [messages[0]] + history + [messages[1]]
    else:
        messages = []
        if system_content:
            messages.append({"role": "system", "content": system_content})
        messages += history

        # CONCEPT · Chain of thought: ask for step-by-step reasoning.
        user_content = question
        if request.cot:
            user_content += (
                "\n\nThink step by step before answering. "
                "Wrap your reasoning in <thinking>...</thinking> "
                "and your final answer in <answer>...</answer>."
            )
        messages.append({"role": "user", "content": user_content})

    # ── CONCEPT · Refusal [Phase 5] ──────────────────────────────────────────
    # Notes exist but nothing matched: say "I don't know" instead of guessing.
    if request.enable_rag and not grounded:
        try:
            from app.vector_store import count
            if count() > 0:
                return AskResponse(
                    answer="I don't have enough information in your notes to answer this.",
                    grounded=False,
                    input_tokens=count_tokens(question),
                    context_report=context_report(messages),
                    injection_detected=injection_detected,
                    pii_detected=pii_detected,
                    pii_types=pii_types,
                    compacted=compacted,
                )
        except Exception:  # noqa: BLE001
            pass

    # ── CONCEPT · Context window [Phase 2.1] ─────────────────────────────────
    # Measure the tokens the prompt uses and warn before we hit the model's limit.
    ctx_warning = context_budget_warning(messages)
    ctx_report  = context_report(messages)

    # ── The model call itself (the one thing v0 already did) ─────────────────
    raw_answer = chat(messages, temperature=request.temperature, top_p=request.top_p)

    # ── CONCEPT · Moderation [Phase 8] — check the model's output too ────────
    if request.enable_security:
        out_mod = moderate(raw_answer)
        if out_mod.get("flagged"):
            raw_answer = "[Response blocked by content policy.]"

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
        append(request.session_id, "user", question)
        append(request.session_id, "assistant", final_answer)

    input_tokens = count_tokens(" ".join(m.get("content") or "" for m in messages))
    return AskResponse(
        answer=final_answer,
        thinking=thinking,
        grounded=grounded,
        sources=sources,
        input_tokens=input_tokens,
        output_tokens=count_tokens(final_answer),
        context_report=ctx_report,
        context_warning=ctx_warning,
        injection_detected=injection_detected,
        pii_detected=pii_detected,
        pii_types=pii_types,
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
# CONCEPT · Embeddings  [Phase 3.2]
# Turn text into a vector; return its size and a preview.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/embed")
def embed_endpoint(body: dict) -> dict:
    from app.embeddings import embed
    vec = embed(body.get("text", ""))
    return {"dimensions": len(vec), "preview": vec[:10], "vector": vec}

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Vector representations  [Phase 3.1]
# Rank toy vectors by cosine similarity -- the idea, by hand.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/similarity-demo")
def similarity_demo() -> list:
    from app.embeddings import DEMO_VECS, rank_by_similarity
    query_vec = [0.88, 0.12, 0.14]  # close to the photosynthesis cluster
    ranked = rank_by_similarity(query_vec, DEMO_VECS)
    return [{"text": t, "score": round(s, 4)} for t, s in ranked]

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Semantic search  [Phase 3.3]
# Rank documents by meaning, not by exact words.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/semantic-search")
def semantic_search_endpoint(body: dict) -> list:
    from app.search import semantic_search
    return semantic_search(body.get("query", ""), body.get("docs", []), int(body.get("k", 3)))

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Indexing  [Phase 4.1]
# Chunk notes and store their vectors in ChromaDB.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/notes/upload")
def upload_note(body: dict) -> dict:
    from app.chunker import chunk_fixed, chunk_paragraph
    from app.vector_store import count, index_document

    filename = body.get("filename", "untitled.md")
    content  = body.get("content", "")
    subject  = body.get("subject", "general")
    strategy = body.get("chunk_strategy", "fixed")   # "fixed" | "paragraph"

    chunks = chunk_paragraph(content) if strategy == "paragraph" else chunk_fixed(content)
    if not chunks:
        chunks = [content]

    for i, chunk in enumerate(chunks):
        index_document(
            chunk,
            metadata={"filename": filename, "subject": subject, "chunk_index": i},
        )
    return {
        "indexed":        True,
        "filename":       filename,
        "chunks_created": len(chunks),
        "total_docs":     count(),
    }

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Similarity search  [Phase 4.2]
# Query the vector store, optionally filtered by subject.
# ────────────────────────────────────────────────────────────────────────────

@app.post("/notes/search")
def search_notes_endpoint(body: dict) -> list:
    from app.vector_store import search
    return search(body.get("query", ""), k=int(body.get("k", 3)), subject=body.get("subject"))

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Agents  [Phase 6]
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
# CONCEPT · MCP  [Phase 7]
# List tools discovered from the MCP server over stdio.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/mcp/tools")
def mcp_tools() -> list:
    """List tools discovered from the Study Buddy MCP server (Phase 7)."""
    from app.mcp_client import list_mcp_tools
    try:
        return list_mcp_tools()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"MCP server unavailable: {exc}")

# ────────────────────────────────────────────────────────────────────────────
# CONCEPT · Frontend  [all phases]
# Serve the single-page UI; every phase of the workshop is driven through it.
# ────────────────────────────────────────────────────────────────────────────

@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
