"""Study Buddy v1 — Personas, CoT reasoning, structured output endpoints."""
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
        user_text += "\n\nThink step by step. Wrap reasoning in <thinking>...</thinking> and answer in <answer>...</answer>."
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
