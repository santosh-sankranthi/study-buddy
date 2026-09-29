"""Generate the app version ladder (v0..v8) as a monotonic sequence.

The whole workshop depends on ``app/main.py`` growing one phase at a time, so
that ``git diff v2 v3`` (or ``switch_version.py``) shows exactly what a phase
added and nothing else. This script is the single source of truth for that
ladder: it composes each version from shared blocks so every step is a clean,
additive diff.

Run it to (re)generate all version snapshots:
    python scripts/build_app_versions.py

The live app (``app/main.py``) is not touched -- use
``python scripts/switch_version.py v8`` to copy a milestone into place.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERSIONS = REPO_ROOT / "app" / "versions"


def _b(text: str) -> str:
    """Normalise a block: strip surrounding blank lines, keep inner content."""
    return text.strip("\n")


def concept(tag: str, title: str, what: str) -> str:
    """Return a comment banner that marks which AI concept a block shows.

    These banners are the teaching map: every meaningful block in the generated
    app is prefixed with the concept it demonstrates, so a student reading
    ``app/versions/vN/main.py`` can follow the story without a guide.
    """
    bar = "# " + "─" * 76
    return f"{bar}\n# CONCEPT · {title}  [{tag}]\n# {what}\n{bar}"


# ─────────────────────────────────────────────────────────────────────────────
# Module docstring (shared by every version)
# ─────────────────────────────────────────────────────────────────────────────

MODULE_DOC = '''"""Study Buddy — the evolving backend.

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
"""'''


# ─────────────────────────────────────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────────────────────────────────────

def imports_for(level: int) -> str:
    lines = [
        "from __future__ import annotations",
        "",
        "import sys",
    ]
    if level >= 1:
        lines.append("import re")
    if level >= 2:
        lines.append("import time")
    if level >= 6:
        lines.append("import json")
        lines.append("import urllib.request")
    lines += [
        "from pathlib import Path",
        "",
        "# Locate the app package by walking up from this file, so this module works",
        "# both as app/main.py and as a snapshot under app/versions/vN/.",
        "_APP_DIR = Path(__file__).resolve()",
        'while _APP_DIR.name != "app" and _APP_DIR.parent != _APP_DIR:',
        "    _APP_DIR = _APP_DIR.parent",
        "sys.path.insert(0, str(_APP_DIR.parent))",
        "",
    ]
    fastapi_imports = "FastAPI"
    if level >= 1:
        fastapi_imports += ", HTTPException"
    lines.append(f"from fastapi import {fastapi_imports}")
    lines.append("from fastapi.responses import FileResponse")
    lines.append("from fastapi.staticfiles import StaticFiles")
    pydantic_imports = "BaseModel"
    if level >= 1:
        pydantic_imports += ", TypeAdapter"
    lines.append(f"from pydantic import {pydantic_imports}")
    lines += [
        "",
        "from common.llm import chat",
        "from common.tokens import count_tokens",
    ]
    if level >= 1:
        lines += [
            "from app.prompts import build_few_shot_prompt, build_system",
            "from app.schemas import Flashcard, QuizItem, StudyPlanDay",
            "from app.tools import TOOLS",
        ]
    if level >= 2:
        lines.append("from app.context import context_budget_warning, context_report")
    if level >= 5:
        lines.append("from app.security import moderate, sanitize_input, scrub_pii")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Request / response models
# ─────────────────────────────────────────────────────────────────────────────

MODELS = {
    0: '''class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str''',
    1: '''class AskRequest(BaseModel):
    question:    str
    mode:        str   = "tutor"
    cot:         bool  = False
    temperature: float = 0.7
    top_p:       float = 1.0


class AskResponse(BaseModel):
    answer:        str
    thinking:      str | None = None
    input_tokens:  int = 0
    output_tokens: int = 0''',
    2: '''class AskRequest(BaseModel):
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
    compacted:       bool = False''',
    5: '''class AskRequest(BaseModel):
    question:         str
    mode:             str        = "tutor"
    cot:              bool       = False
    temperature:      float      = 0.7
    top_p:            float      = 1.0
    session_id:       str | None = None
    student_name:     str | None = None
    study_goal:       str | None = None
    compact_strategy: str        = "halve"   # "halve" | "keep_last2"
    enable_security:  bool       = True      # Phase 5+


class AskResponse(BaseModel):
    answer:             str
    thinking:           str | None = None
    input_tokens:       int = 0
    output_tokens:      int = 0
    context_report:     dict = {}
    context_warning:    str | None = None
    injection_detected: bool = False
    pii_detected:       bool = False
    pii_types:          list[str] = []
    compacted:          bool = False''',
}


def models_for(level: int) -> str:
    if level == 0:
        return MODELS[0]
    if level == 1:
        return MODELS[1]
    if level <= 4:
        return MODELS[2]
    return MODELS[5]


# ─────────────────────────────────────────────────────────────────────────────
# /ask — the evolving core endpoint
# ─────────────────────────────────────────────────────────────────────────────

_ASK_0 = r'''@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Raw one-shot forward pass: no persona, no memory, no grounding."""
    raw = chat(
        [{"role": "user", "content": request.question}],
        temperature=0.7,
    )
    return AskResponse(answer=raw)'''

_ASK_1 = r'''@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Send a question to Study Buddy. Behaviour grows phase by phase."""
    system_content = build_system(mode=request.mode)

    messages: list[dict] = []
    if system_content:
        messages.append({"role": "system", "content": system_content})

    # CONCEPT · Chain of thought: ask for step-by-step reasoning.
    user_content = request.question
    if request.cot:
        user_content += (
            "\n\nThink step by step before answering. "
            "Wrap your reasoning in <thinking>...</thinking> "
            "and your final answer in <answer>...</answer>."
        )
    messages.append({"role": "user", "content": user_content})

    raw_answer = chat(messages, temperature=request.temperature, top_p=request.top_p)

    thinking: str | None = None
    final_answer = raw_answer
    if request.cot:
        t_match = re.search(r"<thinking>(.*?)</thinking>", raw_answer, re.DOTALL)
        a_match = re.search(r"<answer>(.*?)</answer>", raw_answer, re.DOTALL)
        if t_match:
            thinking = t_match.group(1).strip()
        if a_match:
            final_answer = a_match.group(1).strip()

    return AskResponse(
        answer=final_answer,
        thinking=thinking,
        input_tokens=count_tokens(request.question),
        output_tokens=count_tokens(final_answer),
    )'''

_ASK_2 = r'''@app.post("/ask", response_model=AskResponse)
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
    )'''

_ASK_SEC = r'''@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Send a question to Study Buddy. Behaviour grows phase by phase."""

    # ── CONCEPT · Prompt injection + PII [Phase 5] ───────────────────────────
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

    messages: list[dict] = []
    if system_content:
        messages.append({"role": "system", "content": system_content})
    messages += history

    # ── CONCEPT · Chain of thought [Phase 1.3] ───────────────────────────────
    # Ask the model to reason step by step, tagged so we can split it out later.
    user_content = question
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

    # ── CONCEPT · Moderation [Phase 5] — check the model's output too ────────
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
        input_tokens=input_tokens,
        output_tokens=count_tokens(final_answer),
        context_report=ctx_report,
        context_warning=ctx_warning,
        injection_detected=injection_detected,
        pii_detected=pii_detected,
        pii_types=pii_types,
        compacted=compacted,
    )'''


def ask_for(level: int) -> str:
    banner = concept(
        "Phase 0-6",
        "/ask — the core endpoint",
        "One question in, one answer out. Each phase adds one step inside this function.",
    )
    if level == 0:
        body = _ASK_0
    elif level == 1:
        body = _ASK_1
    elif level <= 4:
        body = _ASK_2
    else:
        body = _ASK_SEC
    return banner + "\n\n" + body


# ─────────────────────────────────────────────────────────────────────────────
# Additive endpoint blocks
# ─────────────────────────────────────────────────────────────────────────────

EP_MODES = r'''@app.get("/modes")
def list_modes() -> list[str]:
    return ["tutor", "direct", "flashcard"]'''

EP_QUIZ = r'''QUIZ_EXAMPLES = [
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

    return item.model_dump()'''

EP_FLASHCARDS = r'''@app.post("/flashcards")
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
    return card.model_dump()'''

EP_STUDY_PLAN = r'''@app.post("/study-plan")
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
    return [d.model_dump() for d in plan]'''

EP_TOOLS = r'''@app.get("/tools")
def list_tools() -> list:
    return TOOLS'''

EP_CONTEXT_REPORT = r'''@app.get("/context-report")
def get_context_report(session_id: str | None = None) -> dict:
    messages: list[dict] = []
    if session_id:
        from app.memory import get_history
        messages = get_history(session_id)
    return context_report(messages)'''

EP_SESSION_HISTORY = r'''@app.get("/session/{session_id}/history")
def get_session_history(session_id: str) -> list:
    from app.memory import get_history
    return get_history(session_id)


@app.delete("/session/{session_id}")
def clear_session(session_id: str) -> dict:
    from app.memory import clear
    clear(session_id)
    return {"cleared": True, "session_id": session_id}'''

EP_MEASURE_LONG_CONTEXT = r'''@app.post("/measure-long-context")
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
    return results'''

# NOTE: embeddings / vector store / RAG endpoints were removed with the
# retrieval stack; the code is preserved in archive/rag/.


EP_AGENT_ASK = r'''@app.post("/agent/ask")
def agent_ask(body: dict) -> dict:
    from app.agent import agent_loop
    return agent_loop(body.get("question", ""))


@app.post("/agent/plan-and-execute")
def agent_plan_and_execute(body: dict) -> dict:
    from app.agent import plan_and_execute
    return plan_and_execute(body.get("question", ""))'''

EP_MCP_TOOLS = r'''@app.get("/mcp/tools")
def mcp_tools() -> list:
    """List tools discovered from the Study Buddy MCP server (Phase 7)."""
    from app.mcp_client import list_mcp_tools
    try:
        return list_mcp_tools()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=503, detail=f"MCP server unavailable: {exc}")'''

# NOTE: /eval/groundedness-report was RAG-specific and moved to archive/rag/.


EP_EVAL_REGRESSION = r'''EVAL_SET = [
    {"question": "What is photosynthesis?",              "check": lambda r: "light" in r.lower() or "energy" in r.lower()},
    {"question": "Where does photosynthesis occur?",     "check": lambda r: "chloro" in r.lower()},
    {"question": "What gas does photosynthesis release?", "check": lambda r: "oxygen" in r.lower() or "o2" in r.lower()},
    {"question": "What is Newton's second law?",         "check": lambda r: "f" in r.lower() and "m" in r.lower()},
    {"question": "What is cellular respiration?",        "check": lambda r: "energy" in r.lower() or "atp" in r.lower()},
]


@app.get("/eval/regression-report")
def regression_report() -> dict:
    """Run a mini built-in eval set against a locally running server."""
    passed  = 0
    results = []
    for case in EVAL_SET:
        try:
            payload = json.dumps({
                "question": case["question"],
                "mode":     "direct",
            }).encode()
            req = urllib.request.Request(
                "http://localhost:8000/ask",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
                answer = json.loads(resp.read()).get("answer", "")
            ok = case["check"](answer)
            passed += int(ok)
            results.append({"question": case["question"], "passed": ok})
        except Exception as exc:  # noqa: BLE001
            results.append({"question": case["question"], "passed": False, "error": str(exc)})

    return {
        "total":     len(EVAL_SET),
        "passed":    passed,
        "pass_rate": round(passed / len(EVAL_SET), 3),
        "details":   results,
    }'''


# ─────────────────────────────────────────────────────────────────────────────
# /meta — the capability manifest the frontend uses to adapt the UI
# ─────────────────────────────────────────────────────────────────────────────

def features_for(level: int) -> list[str]:
    """The UI feature flags a version switches on. Grows one phase at a time."""
    feats: list[str] = []
    if level >= 1:
        feats += ["personas", "sampling", "cot", "structured", "tools_schema"]
    if level >= 2:
        feats += ["memory", "context"]
    if level >= 3:
        feats += ["agents"]
    if level >= 4:
        feats += ["mcp"]
    if level >= 5:
        feats += ["security"]
    if level >= 6:
        feats += ["evals"]
    return feats


def meta_endpoint(level: int) -> str:
    banner = concept(
        "all phases",
        "/meta — capability manifest",
        "Report which concepts this version has, so the UI reveals only those controls.",
    )
    return (
        f"{banner}\n"
        '@app.get("/meta")\n'
        "def meta() -> dict:\n"
        '    """What this version supports; the frontend gates its controls on this."""\n'
        "    try:\n"
        "        from common.llm import provider_info\n"
        "        provider = provider_info()\n"
        "    except Exception:  # noqa: BLE001\n"
        "        provider = {}\n"
        f'    return {{"version": "v{level}", "features": {features_for(level)!r}, **provider}}\n'
    )


def endpoints_for(level: int) -> list[str]:
    blocks: list[str] = []
    if level >= 1:
        blocks += [
            concept("Phase 1.1", "Personas / modes",
                    "List the tutor personas the frontend can choose from."),
            EP_MODES,
            concept("Phase 1.2", "Few-shot",
                    "Two worked Q&A -> MCQ examples fix the JSON shape of /quiz-item."),
            EP_QUIZ,
            concept("Phase 1.4", "Structured output",
                    "Pydantic validates the model's JSON, or raises ValidationError."),
            EP_FLASHCARDS,
            concept("Phase 1.4", "Structured output (a list)",
                    "A multi-day plan validated against StudyPlanDay and a time budget."),
            EP_STUDY_PLAN,
            concept("Phase 1.5", "Function calling (schemas)",
                    "Publish the JSON tool contracts; nothing is executed yet."),
            EP_TOOLS,
        ]
    if level >= 2:
        blocks += [
            concept("Phase 2.1", "Context sources",
                    "Show where the prompt's tokens go, broken down by role."),
            EP_CONTEXT_REPORT,
            concept("Phase 2.2", "Memory (API)",
                    "Read or clear a session's stored conversation."),
            EP_SESSION_HISTORY,
            concept("Phase 2.4", "Long context",
                    "Measure latency and cost as the pasted document grows."),
            EP_MEASURE_LONG_CONTEXT,
        ]
    if level >= 3:
        blocks += [
            concept("Phase 3", "Agents",
                    "A ReAct loop that calls tools, plus a planner->executor->critic pipeline."),
            EP_AGENT_ASK,
        ]
    if level >= 4:
        blocks += [
            concept("Phase 4", "MCP",
                    "List tools discovered from the MCP server over stdio."),
            EP_MCP_TOOLS,
        ]
    if level >= 6:
        blocks += [
            concept("Phase 6", "Regression testing",
                    "Run a built-in eval set against the running app."),
            EP_EVAL_REGRESSION,
        ]
    return blocks


# ─────────────────────────────────────────────────────────────────────────────
# Assembly
# ─────────────────────────────────────────────────────────────────────────────

EP_INDEX = concept(
    "all phases",
    "Frontend",
    "Serve the single-page UI; every phase of the workshop is driven through it.",
) + "\n\n" + r'''@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")'''


def compose(level: int) -> str:
    models_block = models_for(level)
    if level >= 1:
        models_block = concept(
            "Phase 1.4",
            "API request / response contract",
            "Pydantic types the request we accept and the response we return.",
        ) + "\n\n" + models_block

    parts = [
        MODULE_DOC,
        imports_for(level),
        'STATIC_DIR = _APP_DIR / "static"',
        f'app = FastAPI(title="Study Buddy", version="v{level}")',
        meta_endpoint(level),
        models_block,
        ask_for(level),
        *endpoints_for(level),
        EP_INDEX,
    ]
    return "\n\n".join(_b(p) for p in parts) + "\n"


def main() -> None:
    for level in range(0, 7):
        target = VERSIONS / f"v{level}" / "main.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(compose(level), encoding="utf-8")
        print(f"wrote {target.relative_to(REPO_ROOT)}")
    print("Rebuilt the v0..v6 app ladder.")


if __name__ == "__main__":
    main()
