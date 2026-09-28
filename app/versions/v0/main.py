"""Study Buddy v0 — Raw one-shot Q&A base.

No system persona, no conversation memory, no vector store, no agents.
"""
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
