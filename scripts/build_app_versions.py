import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
APP = REPO_ROOT / "app"
VERSIONS = APP / "versions"

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ── v0: Raw one-shot Q&A ───────────────────────────────────────────────────────
write(
    VERSIONS / "v0" / "main.py",
    """\"\"\"Study Buddy v0 — Raw one-shot Q&A base.

No system persona, no conversation memory, no vector store, no agents.
\"\"\"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from common.llm import chat

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
app = FastAPI(title="Study Buddy v0")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    # Raw one-shot forward pass
    raw = chat([{"role": "user", "content": req.question}], temperature=0.7)
    return AskResponse(answer=raw)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
"""
)

# ── v1: Prompt Engineering ─────────────────────────────────────────────────────
write(
    VERSIONS / "v1" / "main.py",
    """\"\"\"Study Buddy v1 — Personas, CoT reasoning, structured output endpoints.\"\"\"
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
from app.prompts import TUTOR_SYSTEM_PROMPT, FLASHCARD_SYSTEM_PROMPT, build_few_shot_prompt
from app.schemas import Flashcard, StudyPlanDay

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
app = FastAPI(title="Study Buddy v1")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class AskRequest(BaseModel):
    question: str
    mode: str = "tutor"
    cot: bool = False
    temperature: float = 0.7
    top_p: float = 1.0

class AskResponse(BaseModel):
    answer: str
    thinking: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0

@app.get("/")
def read_root():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    messages = []
    if req.mode == "tutor":
        messages.append({"role": "system", "content": TUTOR_SYSTEM_PROMPT})
    elif req.mode == "flashcard":
        messages.append({"role": "system", "content": FLASHCARD_SYSTEM_PROMPT})

    user_text = req.question
    if req.cot:
        user_text += "\\n\\nThink step by step. Wrap reasoning in <thinking>...</thinking> and answer in <answer>...</answer>."
    messages.append({"role": "user", "content": user_text})

    raw = chat(messages, temperature=req.temperature, top_p=req.top_p)
    thinking = None
    answer = raw
    if req.cot:
        m_t = re.search(r"<thinking>(.*?)</thinking>", raw, re.DOTALL)
        m_a = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
        if m_t: thinking = m_t.group(1).strip()
        if m_a: answer = m_a.group(1).strip()

    return AskResponse(
        answer=answer,
        thinking=thinking,
        input_tokens=count_tokens(req.question),
        output_tokens=count_tokens(answer),
    )

@app.post("/flashcards")
def make_flashcard(body: dict) -> dict:
    card = Flashcard(question=f"Key concept in {body.get('topic')}", answer=f"Definition for {body.get('topic')}", difficulty="medium")
    return card.model_dump()
"""
)

# ── v2: Context Engineering & Memory ───────────────────────────────────────────
write(
    VERSIONS / "v2" / "main.py",
    """\"\"\"Study Buddy v2 — Multi-turn sessions, context budget, compaction, light sanitizer.\"\"\"
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
"""
)

# ── v3..v8: Copy current full app as v8, and snapshot milestones ────────────────
for v in ["v3", "v4", "v5", "v6", "v7", "v8"]:
    target_v = VERSIONS / v
    target_v.mkdir(parents=True, exist_ok=True)
    # Copy current app/main.py as the baseline
    shutil.copy(APP / "main.py", target_v / "main.py")

# Write switch_version.py script
write(
    REPO_ROOT / "scripts" / "switch_version.py",
    """\"\"\"Switch Study Buddy app state to any target version milestone (v0..v8).

Usage:
    python scripts/switch_version.py v0
    python scripts/switch_version.py v4
    python scripts/switch_version.py v8
\"\"\"
import sys
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERSIONS_DIR = REPO_ROOT / "app" / "versions"
MAIN_PY = REPO_ROOT / "app" / "main.py"

def main():
    if len(sys.argv) < 2:
        print("Available versions:")
        for v in sorted(VERSIONS_DIR.iterdir()):
            if v.is_dir():
                print(f"  • {v.name}")
        print("\\nUsage: python scripts/switch_version.py <version_tag>")
        sys.exit(1)

    target_ver = sys.argv[1].strip().lower()
    source_py = VERSIONS_DIR / target_ver / "main.py"
    if not source_py.exists():
        print(f"Error: Version '{target_ver}' not found under {VERSIONS_DIR}")
        sys.exit(1)

    shutil.copy(source_py, MAIN_PY)
    print(f"✅ Switched app/main.py to {target_ver.upper()} milestone successfully.")

if __name__ == "__main__":
    main()
"""
)

print("Created app version snapshots and switcher script successfully.")
