# Study Buddy — Live Workshop Paste Guide

Two clones of this repo: **Clone A (typing)** and **Clone B (showcase)**.

- Clone A: `git switch -c live v0` — this is where you paste, step by step. Never switch it.
- Clone B: read-only; run `git checkout vN` here to show the finished result of each step.
- Both: `pip install -r requirements.txt` once, and copy `.env` with your key.
- Before each run: `python scripts/workshop_reset.py` to clear notes/session state.

Each step below shows the **exact diff** of `app/main.py`. Type the `+` lines into Clone A. If a live paste goes wrong, run the matching `workshop/patches/stepN.patch` with `git apply`. Concepts are numbered so you can explain as you paste.


---

## Step 1 — Phase 1 — Prompt Engineering  ⭐ CORE (2.5h path)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v1`

**Fallback:** `git apply workshop/patches/step1.patch`


### Concepts to explain while you paste

1. **System prompts** (`ask()`) — `build_system()` prepends a persona; the model stops sounding random.

2. **Chain of thought** (`ask()`) — Optional 'think step by step' + `<thinking>` / `<answer>` splitting.

3. **Few-shot** (`QUIZ_EXAMPLES + /quiz-item`) — Two worked examples fix the format of `/quiz-item`.

4. **Structured output** (`/flashcards, /study-plan`) — Pydantic validates the model's JSON in `/flashcards` and `/study-plan`.

5. **Tool schemas** (`/tools, /modes`) — `/tools` publishes the JSON tool contracts — no execution yet.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index 96c6f53..8d911e1 100644
--- a/app/main.py
+++ b/app/main.py
@@ -28,6 +28,7 @@ How to read this file
 from __future__ import annotations
 
 import sys
+import re
 from pathlib import Path
 
 # Locate the app package by walking up from this file, so this module works
@@ -37,17 +38,20 @@ while _APP_DIR.name != "app" and _APP_DIR.parent != _APP_DIR:
     _APP_DIR = _APP_DIR.parent
 sys.path.insert(0, str(_APP_DIR.parent))
 
-from fastapi import FastAPI
+from fastapi import FastAPI, HTTPException
 from fastapi.responses import FileResponse
 from fastapi.staticfiles import StaticFiles
-from pydantic import BaseModel
+from pydantic import BaseModel, TypeAdapter
 
 from common.llm import chat
 from common.tokens import count_tokens
+from app.prompts import build_few_shot_prompt, build_system
+from app.schemas import Flashcard, QuizItem, StudyPlanDay
+from app.tools import TOOLS
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v0")
+app = FastAPI(title="Study Buddy", version="v1")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -56,14 +60,26 @@ app = FastAPI(title="Study Buddy", version="v0")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v0", "features": []}
+    return {"version": "v1", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema']}
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · API request / response contract  [Phase 1.4]
+# Pydantic types the request we accept and the response we return.
+# ────────────────────────────────────────────────────────────────────────────
 
 class AskRequest(BaseModel):
-    question: str
+    question:    str
+    mode:        str   = "tutor"
+    cot:         bool  = False
+    temperature: float = 0.7
+    top_p:       float = 1.0
 
 
 class AskResponse(BaseModel):
-    answer: str
+    answer:        str
+    thinking:      str | None = None
+    input_tokens:  int = 0
+    output_tokens: int = 0
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /ask — the core endpoint  [Phase 0-9]
@@ -72,12 +88,158 @@ class AskResponse(BaseModel):
 
 @app.post("/ask", response_model=AskResponse)
 def ask(request: AskRequest) -> AskResponse:
-    """Raw one-shot forward pass: no persona, no memory, no grounding."""
-    raw = chat(
-        [{"role": "user", "content": request.question}],
-        temperature=0.7,
+    """Send a question to Study Buddy. Behaviour grows phase by phase."""
+    system_content = build_system(mode=request.mode)
+
+    messages: list[dict] = []
+    if system_content:
+        messages.append({"role": "system", "content": system_content})
+
+    # CONCEPT · Chain of thought: ask for step-by-step reasoning.
+    user_content = request.question
+    if request.cot:
+        user_content += (
+            "\n\nThink step by step before answering. "
+            "Wrap your reasoning in <thinking>...</thinking> "
+            "and your final answer in <answer>...</answer>."
+        )
+    messages.append({"role": "user", "content": user_content})
+
+    raw_answer = chat(messages, temperature=request.temperature, top_p=request.top_p)
+
+    thinking: str | None = None
+    final_answer = raw_answer
+    if request.cot:
+        t_match = re.search(r"<thinking>(.*?)</thinking>", raw_answer, re.DOTALL)
+        a_match = re.search(r"<answer>(.*?)</answer>", raw_answer, re.DOTALL)
+        if t_match:
+            thinking = t_match.group(1).strip()
+        if a_match:
+            final_answer = a_match.group(1).strip()
+
+    return AskResponse(
+        answer=final_answer,
+        thinking=thinking,
+        input_tokens=count_tokens(request.question),
+        output_tokens=count_tokens(final_answer),
     )
-    return AskResponse(answer=raw)
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Personas / modes  [Phase 1.1]
+# List the tutor personas the frontend can choose from.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/modes")
+def list_modes() -> list[str]:
+    return ["tutor", "direct", "flashcard"]
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Few-shot  [Phase 1.2]
+# Two worked Q&A -> MCQ examples fix the JSON shape of /quiz-item.
+# ────────────────────────────────────────────────────────────────────────────
+
+QUIZ_EXAMPLES = [
+    {
+        "input":  "Photosynthesis",
+        "output": (
+            '{"question": "Where does photosynthesis occur?", '
+            '"options": ["Mitochondria", "Chloroplast", "Nucleus", "Ribosome"], '
+            '"correct_index": 1}'
+        ),
+    },
+    {
+        "input":  "Newton\'s first law",
+        "output": (
+            '{"question": "What does Newton\'s first law state?", '
+            '"options": ["F = ma", "Objects in motion stay in motion unless acted on", '
+            '"Every action has an equal reaction", "Gravity attracts masses"], '
+            '"correct_index": 1}'
+        ),
+    },
+]
+
+
+@app.post("/quiz-item")
+def make_quiz_item(body: dict) -> dict:
+    topic    = body.get("topic", "")
+    messages = [
+        {"role": "system", "content": "Return ONLY a valid JSON object matching the QuizItem schema. No other text."},
+    ] + build_few_shot_prompt(QUIZ_EXAMPLES, topic)
+    raw  = chat(messages, temperature=0.3)
+    item = QuizItem.model_validate_json(raw)
+
+    session_id = body.get("session_id")
+    if session_id:
+        from app.memory import add_quiz_item
+        add_quiz_item(session_id, item.model_dump())
+
+    return item.model_dump()
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Structured output  [Phase 1.4]
+# Pydantic validates the model's JSON, or raises ValidationError.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/flashcards")
+def make_flashcards(body: dict) -> dict:
+    topic = body.get("topic", "")
+    messages = [
+        {
+            "role":    "system",
+            "content": (
+                'Return a valid JSON object: {"question":"...","answer":"...","difficulty":"easy|medium|hard"}. '
+                "No other text, no markdown fences."
+            ),
+        },
+        {"role": "user", "content": f"Topic: {topic}"},
+    ]
+    raw  = chat(messages, temperature=0.3)
+    card = Flashcard.model_validate_json(raw)
+    return card.model_dump()
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Structured output (a list)  [Phase 1.4]
+# A multi-day plan validated against StudyPlanDay and a time budget.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/study-plan")
+def make_study_plan(body: dict) -> list:
+    subjects    = body.get("subjects", [])
+    total_hours = body.get("total_hours", 4)
+    messages = [
+        {
+            "role":    "system",
+            "content": (
+                "Return a valid JSON array of StudyPlanDay objects. "
+                'Each object: {"subject":"...","topics":["..."],"minutes":<int>}. '
+                f"Total minutes must not exceed {total_hours * 60}. "
+                "No other text, no markdown fences."
+            ),
+        },
+        {
+            "role":    "user",
+            "content": f"Subjects: {', '.join(subjects)}. Total hours available: {total_hours}.",
+        },
+    ]
+    raw  = chat(messages, temperature=0.3)
+    ta   = TypeAdapter(list[StudyPlanDay])
+    plan = ta.validate_json(raw)
+    total_mins = sum(d.minutes for d in plan)
+    if total_mins > total_hours * 60:
+        raise HTTPException(
+            status_code=422,
+            detail=f"Study plan exceeds the time budget: {total_mins} > {total_hours * 60} minutes.",
+        )
+    return [d.model_dump() for d in plan]
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Function calling (schemas)  [Phase 1.5]
+# Publish the JSON tool contracts; nothing is executed yet.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/tools")
+def list_tools() -> list:
+    return TOOLS
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · Frontend  [all phases]
```


---

## Step 2 — Phase 2 — Context Engineering  ⭐ CORE (2.5h path)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v2`

**Fallback:** `git apply workshop/patches/step2.patch`


### Concepts to explain while you paste

1. **Context sources** (`ask() + /context-report`) — `context_report()` shows where every token goes.

2. **Memory** (`ask() + /session/{id}`) — Session history is reloaded each turn so it remembers.

3. **Context compaction** (`ask()`) — Long history is summarised instead of overflowing.

4. **Long context** (`/measure-long-context`) — Measure latency/cost as the document grows.

5. **Context security** (`sanitize (Phase 2 light pass)`) — Obvious injection is stripped before it reaches the model.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index 8d911e1..be22f51 100644
--- a/app/main.py
+++ b/app/main.py
@@ -29,6 +29,8 @@ from __future__ import annotations
 
 import sys
 import re
+import time
+import urllib.request
 from pathlib import Path
 
 # Locate the app package by walking up from this file, so this module works
@@ -48,10 +50,11 @@ from common.tokens import count_tokens
 from app.prompts import build_few_shot_prompt, build_system
 from app.schemas import Flashcard, QuizItem, StudyPlanDay
 from app.tools import TOOLS
+from app.context import context_budget_warning, context_report
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v1")
+app = FastAPI(title="Study Buddy", version="v2")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -60,7 +63,7 @@ app = FastAPI(title="Study Buddy", version="v1")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v1", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema']}
+    return {"version": "v2", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -68,18 +71,25 @@ def meta() -> dict:
 # ────────────────────────────────────────────────────────────────────────────
 
 class AskRequest(BaseModel):
-    question:    str
-    mode:        str   = "tutor"
-    cot:         bool  = False
-    temperature: float = 0.7
-    top_p:       float = 1.0
+    question:         str
+    mode:             str        = "tutor"
+    cot:              bool       = False
+    temperature:      float      = 0.7
+    top_p:            float      = 1.0
+    session_id:       str | None = None
+    student_name:     str | None = None
+    study_goal:       str | None = None
+    compact_strategy: str        = "halve"   # "halve" | "keep_last2"
 
 
 class AskResponse(BaseModel):
-    answer:        str
-    thinking:      str | None = None
-    input_tokens:  int = 0
-    output_tokens: int = 0
+    answer:          str
+    thinking:        str | None = None
+    input_tokens:    int = 0
+    output_tokens:   int = 0
+    context_report:  dict = {}
+    context_warning: str | None = None
+    compacted:       bool = False
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /ask — the core endpoint  [Phase 0-9]
@@ -89,13 +99,36 @@ class AskResponse(BaseModel):
 @app.post("/ask", response_model=AskResponse)
 def ask(request: AskRequest) -> AskResponse:
     """Send a question to Study Buddy. Behaviour grows phase by phase."""
-    system_content = build_system(mode=request.mode)
+
+    # ── CONCEPT · Memory [Phase 2.2] ─────────────────────────────────────────
+    # Reload earlier turns so the tutor remembers. Compaction shrinks long history.
+    compacted = False
+    history: list[dict] = []
+    if request.session_id:
+        from app.memory import (
+            append, compact_if_needed, compact_keep_last2, get_history,
+        )
+        if request.compact_strategy == "keep_last2":
+            compacted = compact_keep_last2(request.session_id)
+        else:
+            compacted = compact_if_needed(request.session_id)
+        history = get_history(request.session_id)
+
+    # ── CONCEPT · System prompt [Phase 1.1] ──────────────────────────────────
+    # Prepend a `system` message: who the tutor is and the rules it must follow.
+    system_content = build_system(
+        mode=request.mode,
+        student_name=request.student_name,
+        study_goal=request.study_goal,
+    )
 
     messages: list[dict] = []
     if system_content:
         messages.append({"role": "system", "content": system_content})
+    messages += history
 
-    # CONCEPT · Chain of thought: ask for step-by-step reasoning.
+    # ── CONCEPT · Chain of thought [Phase 1.3] ───────────────────────────────
+    # Ask the model to reason step by step, tagged so we can split it out later.
     user_content = request.question
     if request.cot:
         user_content += (
@@ -105,8 +138,15 @@ def ask(request: AskRequest) -> AskResponse:
         )
     messages.append({"role": "user", "content": user_content})
 
+    # ── CONCEPT · Context window [Phase 2.1] ─────────────────────────────────
+    # Measure the tokens the prompt uses and warn before we hit the model's limit.
+    ctx_warning = context_budget_warning(messages)
+    ctx_report  = context_report(messages)
+
+    # ── The model call itself (the one thing v0 already did) ─────────────────
     raw_answer = chat(messages, temperature=request.temperature, top_p=request.top_p)
 
+    # ── CONCEPT · Chain of thought — separate reasoning from the answer ──────
     thinking: str | None = None
     final_answer = raw_answer
     if request.cot:
@@ -117,11 +157,20 @@ def ask(request: AskRequest) -> AskResponse:
         if a_match:
             final_answer = a_match.group(1).strip()
 
+    # ── CONCEPT · Memory — store this turn so the next one remembers it ──────
+    if request.session_id:
+        append(request.session_id, "user", request.question)
+        append(request.session_id, "assistant", final_answer)
+
+    input_tokens = count_tokens(" ".join(m.get("content") or "" for m in messages))
     return AskResponse(
         answer=final_answer,
         thinking=thinking,
-        input_tokens=count_tokens(request.question),
+        input_tokens=input_tokens,
         output_tokens=count_tokens(final_answer),
+        context_report=ctx_report,
+        context_warning=ctx_warning,
+        compacted=compacted,
     )
 
 # ────────────────────────────────────────────────────────────────────────────
@@ -241,6 +290,70 @@ def make_study_plan(body: dict) -> list:
 def list_tools() -> list:
     return TOOLS
 
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Context sources  [Phase 2.1]
+# Show where the prompt's tokens go, broken down by role.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/context-report")
+def get_context_report(session_id: str | None = None) -> dict:
+    messages: list[dict] = []
+    if session_id:
+        from app.memory import get_history
+        messages = get_history(session_id)
+    return context_report(messages)
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Memory (API)  [Phase 2.2]
+# Read or clear a session's stored conversation.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/session/{session_id}/history")
+def get_session_history(session_id: str) -> list:
+    from app.memory import get_history
+    return get_history(session_id)
+
+
+@app.delete("/session/{session_id}")
+def clear_session(session_id: str) -> dict:
+    from app.memory import clear
+    clear(session_id)
+    return {"cleared": True, "session_id": session_id}
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Long context  [Phase 2.4]
+# Measure latency and cost as the pasted document grows.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/measure-long-context")
+def measure_long_context(body: dict) -> list:
+    """Measure latency and cost as document token count grows in steps."""
+    import tiktoken
+    doc_text = body.get("text", "")
+    question = "Summarise the above in one sentence."
+    enc      = tiktoken.get_encoding("cl100k_base")
+    results  = []
+
+    PRICE_PER_M_TOKENS = 0.50  # approximate — adjust to the model's real price
+
+    for tokens_target in [500, 1_000, 2_000, 4_000]:
+        ids   = enc.encode(doc_text)[:tokens_target]
+        text  = enc.decode(ids)
+        msgs  = [{"role": "user", "content": text + "\n\n" + question}]
+
+        t0      = time.monotonic()
+        _       = chat(msgs, temperature=0.0)
+        latency = round((time.monotonic() - t0) * 1_000)
+
+        actual_tokens = len(ids)
+        results.append({
+            "target_tokens": tokens_target,
+            "actual_tokens": actual_tokens,
+            "latency_ms":    latency,
+            "est_cost_usd":  round(actual_tokens / 1_000_000 * PRICE_PER_M_TOKENS, 6),
+        })
+    return results
+
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · Frontend  [all phases]
 # Serve the single-page UI; every phase of the workshop is driven through it.
```


---

## Step 3 — Phases 3+4 — Embeddings & Vector Database  ⭐ CORE (2.5h path)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v3`

**Fallback:** `git apply workshop/patches/step3.patch`


### Concepts to explain while you paste

1. **Vector representations** (`/similarity-demo`) — `/similarity-demo` ranks toy vectors by cosine similarity.

2. **Embedding models** (`/embed`) — `/embed` turns text into a real vector.

3. **Semantic search** (`/semantic-search`) — `/semantic-search` ranks docs by meaning, not words.

4. **Indexing** (`/notes/upload`) — `/notes/upload` chunks and stores notes in ChromaDB.

5. **Similarity search** (`/notes/search`) — `/notes/search` retrieves chunks, with metadata filtering.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index be22f51..c24fe8b 100644
--- a/app/main.py
+++ b/app/main.py
@@ -54,7 +54,7 @@ from app.context import context_budget_warning, context_report
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v2")
+app = FastAPI(title="Study Buddy", version="v3")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -63,7 +63,7 @@ app = FastAPI(title="Study Buddy", version="v2")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v2", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context']}
+    return {"version": "v3", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -354,6 +354,80 @@ def measure_long_context(body: dict) -> list:
         })
     return results
 
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Embeddings  [Phase 3.2]
+# Turn text into a vector; return its size and a preview.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/embed")
+def embed_endpoint(body: dict) -> dict:
+    from app.embeddings import embed
+    vec = embed(body.get("text", ""))
+    return {"dimensions": len(vec), "preview": vec[:10], "vector": vec}
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Vector representations  [Phase 3.1]
+# Rank toy vectors by cosine similarity -- the idea, by hand.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/similarity-demo")
+def similarity_demo() -> list:
+    from app.embeddings import DEMO_VECS, rank_by_similarity
+    query_vec = [0.88, 0.12, 0.14]  # close to the photosynthesis cluster
+    ranked = rank_by_similarity(query_vec, DEMO_VECS)
+    return [{"text": t, "score": round(s, 4)} for t, s in ranked]
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Semantic search  [Phase 3.3]
+# Rank documents by meaning, not by exact words.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/semantic-search")
+def semantic_search_endpoint(body: dict) -> list:
+    from app.search import semantic_search
+    return semantic_search(body.get("query", ""), body.get("docs", []), int(body.get("k", 3)))
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Indexing  [Phase 4.1]
+# Chunk notes and store their vectors in ChromaDB.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/notes/upload")
+def upload_note(body: dict) -> dict:
+    from app.chunker import chunk_fixed, chunk_paragraph
+    from app.vector_store import count, index_document
+
+    filename = body.get("filename", "untitled.md")
+    content  = body.get("content", "")
+    subject  = body.get("subject", "general")
+    strategy = body.get("chunk_strategy", "fixed")   # "fixed" | "paragraph"
+
+    chunks = chunk_paragraph(content) if strategy == "paragraph" else chunk_fixed(content)
+    if not chunks:
+        chunks = [content]
+
+    for i, chunk in enumerate(chunks):
+        index_document(
+            chunk,
+            metadata={"filename": filename, "subject": subject, "chunk_index": i},
+        )
+    return {
+        "indexed":        True,
+        "filename":       filename,
+        "chunks_created": len(chunks),
+        "total_docs":     count(),
+    }
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Similarity search  [Phase 4.2]
+# Query the vector store, optionally filtered by subject.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/notes/search")
+def search_notes_endpoint(body: dict) -> list:
+    from app.vector_store import search
+    return search(body.get("query", ""), k=int(body.get("k", 3)), subject=body.get("subject"))
+
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · Frontend  [all phases]
 # Serve the single-page UI; every phase of the workshop is driven through it.
```


---

## Step 4 — Phase 5 — RAG  ⭐ CORE (2.5h path)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v4`

**Fallback:** `git apply workshop/patches/step4.patch`


### Concepts to explain while you paste

1. **Retrieval + generation** (`ask()`) — `/ask` now retrieves notes and answers only from them.

2. **Grounding + citations** (`ask()`) — The answer must cite `[Chunk N — file]`.

3. **Refusal** (`ask()`) — No relevant note → it says so instead of guessing.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index c24fe8b..5d42576 100644
--- a/app/main.py
+++ b/app/main.py
@@ -54,7 +54,7 @@ from app.context import context_budget_warning, context_report
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v3")
+app = FastAPI(title="Study Buddy", version="v4")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -63,7 +63,7 @@ app = FastAPI(title="Study Buddy", version="v3")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v3", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes']}
+    return {"version": "v4", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -80,11 +80,14 @@ class AskRequest(BaseModel):
     student_name:     str | None = None
     study_goal:       str | None = None
     compact_strategy: str        = "halve"   # "halve" | "keep_last2"
+    enable_rag:       bool       = True      # Phase 4+
 
 
 class AskResponse(BaseModel):
     answer:          str
     thinking:        str | None = None
+    grounded:        bool = False
+    sources:         list[str] = []
     input_tokens:    int = 0
     output_tokens:   int = 0
     context_report:  dict = {}
@@ -122,21 +125,62 @@ def ask(request: AskRequest) -> AskResponse:
         study_goal=request.study_goal,
     )
 
-    messages: list[dict] = []
-    if system_content:
-        messages.append({"role": "system", "content": system_content})
-    messages += history
-
-    # ── CONCEPT · Chain of thought [Phase 1.3] ───────────────────────────────
-    # Ask the model to reason step by step, tagged so we can split it out later.
-    user_content = request.question
-    if request.cot:
-        user_content += (
-            "\n\nThink step by step before answering. "
-            "Wrap your reasoning in <thinking>...</thinking> "
-            "and your final answer in <answer>...</answer>."
-        )
-    messages.append({"role": "user", "content": user_content})
+    # ── CONCEPT · Retrieval [Phase 5] ────────────────────────────────────────
+    # Semantic-search the notes for the most relevant chunks; None = nothing close.
+    grounded = False
+    sources: list[str] = []
+    rag_chunks: list[dict] = []
+    if request.enable_rag:
+        try:
+            from app.vector_store import retrieve
+            from app.rag import extract_sources
+            chunks = retrieve(request.question, k=3)
+            if chunks:
+                rag_chunks = chunks
+                sources    = extract_sources(chunks)
+                grounded   = True
+        except Exception:  # noqa: BLE001 — RAG not set up yet is fine
+            pass
+
+    # ── CONCEPT · Grounded generation [Phase 5] ──────────────────────────────
+    # If we retrieved notes, build a prompt that answers ONLY from those chunks.
+    if grounded and rag_chunks:
+        from app.rag import build_rag_prompt
+        messages = build_rag_prompt(request.question, rag_chunks)
+        # Prepend history before the RAG user message.
+        if history:
+            messages = [messages[0]] + history + [messages[1]]
+    else:
+        messages = []
+        if system_content:
+            messages.append({"role": "system", "content": system_content})
+        messages += history
+
+        # CONCEPT · Chain of thought: ask for step-by-step reasoning.
+        user_content = request.question
+        if request.cot:
+            user_content += (
+                "\n\nThink step by step before answering. "
+                "Wrap your reasoning in <thinking>...</thinking> "
+                "and your final answer in <answer>...</answer>."
+            )
+        messages.append({"role": "user", "content": user_content})
+
+    # ── CONCEPT · Refusal [Phase 5] ──────────────────────────────────────────
+    # Notes exist but nothing matched: say "I don't know" instead of guessing.
+    if request.enable_rag and not grounded:
+        try:
+            from app.vector_store import count
+            if count() > 0:
+                return AskResponse(
+                    answer="I don't have enough information in your notes to answer this.",
+                    grounded=False,
+                    input_tokens=count_tokens(request.question),
+                    context_report=context_report(messages),
+                    compacted=compacted,
+                )
+        except Exception:  # noqa: BLE001
+            pass
 
     # ── CONCEPT · Context window [Phase 2.1] ─────────────────────────────────
     # Measure the tokens the prompt uses and warn before we hit the model's limit.
@@ -166,6 +210,8 @@ def ask(request: AskRequest) -> AskResponse:
     return AskResponse(
         answer=final_answer,
         thinking=thinking,
+        grounded=grounded,
+        sources=sources,
         input_tokens=input_tokens,
         output_tokens=count_tokens(final_answer),
         context_report=ctx_report,
```


---

## Step 5 — Phase 6 — Agents & Tools  (extension)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v5`

**Fallback:** `git apply workshop/patches/step5.patch`


### Concepts to explain while you paste

1. **Tools + function calling** (`/agent/ask`) — Real functions in `TOOL_REGISTRY` are executed.

2. **ReAct loop** (`/agent/ask`) — Think → act → observe, with a visible trace.

3. **Agent loops** (`app/agent.py`) — Stop conditions: step cap + repeat detection.

4. **Multi-agent** (`/agent/plan-and-execute`) — Planner → executor → critic.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index 5d42576..f17ad63 100644
--- a/app/main.py
+++ b/app/main.py
@@ -54,7 +54,7 @@ from app.context import context_budget_warning, context_report
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v4")
+app = FastAPI(title="Study Buddy", version="v5")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -63,7 +63,7 @@ app = FastAPI(title="Study Buddy", version="v4")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v4", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag']}
+    return {"version": "v5", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -474,6 +474,22 @@ def search_notes_endpoint(body: dict) -> list:
     from app.vector_store import search
     return search(body.get("query", ""), k=int(body.get("k", 3)), subject=body.get("subject"))
 
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Agents  [Phase 6]
+# A ReAct loop that calls tools, plus a planner->executor->critic pipeline.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.post("/agent/ask")
+def agent_ask(body: dict) -> dict:
+    from app.agent import agent_loop
+    return agent_loop(body.get("question", ""))
+
+
+@app.post("/agent/plan-and-execute")
+def agent_plan_and_execute(body: dict) -> dict:
+    from app.agent import plan_and_execute
+    return plan_and_execute(body.get("question", ""))
+
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · Frontend  [all phases]
 # Serve the single-page UI; every phase of the workshop is driven through it.
```


---

## Step 6 — Phase 7 — MCP  (extension)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v6`

**Fallback:** `git apply workshop/patches/step6.patch`


### Concepts to explain while you paste

1. **Servers / tools / resources** (`mcp_server/server.py`) — Tools and the notes corpus exposed over MCP.

2. **Clients** (`/mcp/tools`) — Study Buddy discovers tools via `/mcp/tools`.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index f17ad63..6cef11e 100644
--- a/app/main.py
+++ b/app/main.py
@@ -54,7 +54,7 @@ from app.context import context_budget_warning, context_report
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v5")
+app = FastAPI(title="Study Buddy", version="v6")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -63,7 +63,7 @@ app = FastAPI(title="Study Buddy", version="v5")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v5", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents']}
+    return {"version": "v6", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents', 'mcp']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -490,6 +490,20 @@ def agent_plan_and_execute(body: dict) -> dict:
     from app.agent import plan_and_execute
     return plan_and_execute(body.get("question", ""))
 
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · MCP  [Phase 7]
+# List tools discovered from the MCP server over stdio.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/mcp/tools")
+def mcp_tools() -> list:
+    """List tools discovered from the Study Buddy MCP server (Phase 7)."""
+    from app.mcp_client import list_mcp_tools
+    try:
+        return list_mcp_tools()
+    except Exception as exc:  # noqa: BLE001
+        raise HTTPException(status_code=503, detail=f"MCP server unavailable: {exc}")
+
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · Frontend  [all phases]
 # Serve the single-page UI; every phase of the workshop is driven through it.
```


---

## Step 7 — Phase 8 — AI Safety  (extension)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v7`

**Fallback:** `git apply workshop/patches/step7.patch`


### Concepts to explain while you paste

1. **Prompt injection** (`ask()`) — Retrieved chunks are fenced as untrusted data.

2. **Privacy** (`ask()`) — Emails / phones / cards are redacted before sending.

3. **Moderation** (`ask()`) — Input and output are checked by `moderate()`.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index 6cef11e..4841c68 100644
--- a/app/main.py
+++ b/app/main.py
@@ -51,10 +51,11 @@ from app.prompts import build_few_shot_prompt, build_system
 from app.schemas import Flashcard, QuizItem, StudyPlanDay
 from app.tools import TOOLS
 from app.context import context_budget_warning, context_report
+from app.security import moderate, sanitize_input, scrub_pii
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v6")
+app = FastAPI(title="Study Buddy", version="v7")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -63,7 +64,7 @@ app = FastAPI(title="Study Buddy", version="v6")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v6", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents', 'mcp']}
+    return {"version": "v7", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents', 'mcp', 'security']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -81,18 +82,22 @@ class AskRequest(BaseModel):
     study_goal:       str | None = None
     compact_strategy: str        = "halve"   # "halve" | "keep_last2"
     enable_rag:       bool       = True      # Phase 4+
+    enable_security:  bool       = True      # Phase 7+
 
 
 class AskResponse(BaseModel):
-    answer:          str
-    thinking:        str | None = None
-    grounded:        bool = False
-    sources:         list[str] = []
-    input_tokens:    int = 0
-    output_tokens:   int = 0
-    context_report:  dict = {}
-    context_warning: str | None = None
-    compacted:       bool = False
+    answer:             str
+    thinking:           str | None = None
+    grounded:           bool = False
+    sources:            list[str] = []
+    input_tokens:       int = 0
+    output_tokens:      int = 0
+    context_report:     dict = {}
+    context_warning:    str | None = None
+    injection_detected: bool = False
+    pii_detected:       bool = False
+    pii_types:          list[str] = []
+    compacted:          bool = False
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /ask — the core endpoint  [Phase 0-9]
@@ -103,6 +108,25 @@ class AskResponse(BaseModel):
 def ask(request: AskRequest) -> AskResponse:
     """Send a question to Study Buddy. Behaviour grows phase by phase."""
 
+    # ── CONCEPT · Prompt injection + PII [Phase 8] ───────────────────────────
+    # Strip injected instructions and redact personal data before anything runs.
+    question           = request.question
+    injection_detected = False
+    pii_detected       = False
+    pii_types: list[str] = []
+
+    if request.enable_security:
+        question, injection_detected = sanitize_input(question)
+        question, pii_types          = scrub_pii(question)
+        pii_detected                 = bool(pii_types)
+
+        input_mod = moderate(question)
+        if input_mod.get("flagged"):
+            raise HTTPException(
+                status_code=422,
+                detail=f"Request blocked by content policy. Categories: {input_mod.get('categories', {})}",
+            )
+
     # ── CONCEPT · Memory [Phase 2.2] ─────────────────────────────────────────
     # Reload earlier turns so the tutor remembers. Compaction shrinks long history.
     compacted = False
@@ -134,7 +158,7 @@ def ask(request: AskRequest) -> AskResponse:
         try:
             from app.vector_store import retrieve
             from app.rag import extract_sources
-            chunks = retrieve(request.question, k=3)
+            chunks = retrieve(question, k=3)
             if chunks:
                 rag_chunks = chunks
                 sources    = extract_sources(chunks)
@@ -146,7 +170,7 @@ def ask(request: AskRequest) -> AskResponse:
     # If we retrieved notes, build a prompt that answers ONLY from those chunks.
     if grounded and rag_chunks:
         from app.rag import build_rag_prompt
-        messages = build_rag_prompt(request.question, rag_chunks)
+        messages = build_rag_prompt(question, rag_chunks)
         # Prepend history before the RAG user message.
         if history:
             messages = [messages[0]] + history + [messages[1]]
@@ -157,7 +181,7 @@ def ask(request: AskRequest) -> AskResponse:
         messages += history
 
         # CONCEPT · Chain of thought: ask for step-by-step reasoning.
-        user_content = request.question
+        user_content = question
         if request.cot:
             user_content += (
                 "\n\nThink step by step before answering. "
@@ -175,8 +199,11 @@ def ask(request: AskRequest) -> AskResponse:
                 return AskResponse(
                     answer="I don't have enough information in your notes to answer this.",
                     grounded=False,
-                    input_tokens=count_tokens(request.question),
+                    input_tokens=count_tokens(question),
                     context_report=context_report(messages),
+                    injection_detected=injection_detected,
+                    pii_detected=pii_detected,
+                    pii_types=pii_types,
                     compacted=compacted,
                 )
         except Exception:  # noqa: BLE001
@@ -190,6 +217,12 @@ def ask(request: AskRequest) -> AskResponse:
     # ── The model call itself (the one thing v0 already did) ─────────────────
     raw_answer = chat(messages, temperature=request.temperature, top_p=request.top_p)
 
+    # ── CONCEPT · Moderation [Phase 8] — check the model's output too ────────
+    if request.enable_security:
+        out_mod = moderate(raw_answer)
+        if out_mod.get("flagged"):
+            raw_answer = "[Response blocked by content policy.]"
+
     # ── CONCEPT · Chain of thought — separate reasoning from the answer ──────
     thinking: str | None = None
     final_answer = raw_answer
@@ -203,7 +236,7 @@ def ask(request: AskRequest) -> AskResponse:
 
     # ── CONCEPT · Memory — store this turn so the next one remembers it ──────
     if request.session_id:
-        append(request.session_id, "user", request.question)
+        append(request.session_id, "user", question)
         append(request.session_id, "assistant", final_answer)
 
     input_tokens = count_tokens(" ".join(m.get("content") or "" for m in messages))
@@ -216,6 +249,9 @@ def ask(request: AskRequest) -> AskResponse:
         output_tokens=count_tokens(final_answer),
         context_report=ctx_report,
         context_warning=ctx_warning,
+        injection_detected=injection_detected,
+        pii_detected=pii_detected,
+        pii_types=pii_types,
         compacted=compacted,
     )
 
```


---

## Step 8 — Phase 9 — Evaluation & Observability  (extension)

**Clone A:** paste the changes below into `app/main.py`.

**Clone B:** `git checkout v8`

**Fallback:** `git apply workshop/patches/step8.patch`


### Concepts to explain while you paste

1. **Groundedness report** (`/eval/groundedness-report`) — Pass rate over logged groundedness checks.

2. **Regression report** (`/eval/regression-report`) — A built-in eval set scored against the running app.


### The exact change (`app/main.py`)

```diff
diff --git a/app/main.py b/app/main.py
index 4841c68..aa9a836 100644
--- a/app/main.py
+++ b/app/main.py
@@ -31,6 +31,7 @@ import sys
 import re
 import time
 import urllib.request
+import json
 from pathlib import Path
 
 # Locate the app package by walking up from this file, so this module works
@@ -55,7 +56,7 @@ from app.security import moderate, sanitize_input, scrub_pii
 
 STATIC_DIR = _APP_DIR / "static"
 
-app = FastAPI(title="Study Buddy", version="v7")
+app = FastAPI(title="Study Buddy", version="v8")
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · /meta — capability manifest  [all phases]
@@ -64,7 +65,7 @@ app = FastAPI(title="Study Buddy", version="v7")
 @app.get("/meta")
 def meta() -> dict:
     """What this version supports; the frontend gates its controls on this."""
-    return {"version": "v7", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents', 'mcp', 'security']}
+    return {"version": "v8", "features": ['personas', 'sampling', 'cot', 'structured', 'tools_schema', 'memory', 'context', 'embeddings', 'notes', 'rag', 'agents', 'mcp', 'security', 'evals']}
 
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · API request / response contract  [Phase 1.4]
@@ -540,6 +541,70 @@ def mcp_tools() -> list:
     except Exception as exc:  # noqa: BLE001
         raise HTTPException(status_code=503, detail=f"MCP server unavailable: {exc}")
 
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Observability  [Phase 9.5]
+# Pass rate over logged groundedness checks.
+# ────────────────────────────────────────────────────────────────────────────
+
+@app.get("/eval/groundedness-report")
+def groundedness_report() -> dict:
+    log_path = Path("./data/groundedness_log.jsonl")
+    if not log_path.exists():
+        return {"checked": 0, "passed": 0, "pass_rate": 0.0}
+    lines  = [json.loads(line) for line in log_path.read_text().splitlines() if line.strip()]
+    passed = sum(1 for line in lines if line.get("grounded"))
+    return {
+        "checked":   len(lines),
+        "passed":    passed,
+        "pass_rate": round(passed / len(lines), 3) if lines else 0.0,
+    }
+
+# ────────────────────────────────────────────────────────────────────────────
+# CONCEPT · Regression testing  [Phase 9.4]
+# Run a built-in eval set against the running app.
+# ────────────────────────────────────────────────────────────────────────────
+
+EVAL_SET = [
+    {"question": "What is photosynthesis?",              "check": lambda r: "light" in r.lower() or "energy" in r.lower()},
+    {"question": "Where does photosynthesis occur?",     "check": lambda r: "chloro" in r.lower()},
+    {"question": "What gas does photosynthesis release?", "check": lambda r: "oxygen" in r.lower() or "o2" in r.lower()},
+    {"question": "What is Newton's second law?",         "check": lambda r: "f" in r.lower() and "m" in r.lower()},
+    {"question": "What is cellular respiration?",        "check": lambda r: "energy" in r.lower() or "atp" in r.lower()},
+]
+
+
+@app.get("/eval/regression-report")
+def regression_report() -> dict:
+    """Run a mini built-in eval set against a locally running server."""
+    passed  = 0
+    results = []
+    for case in EVAL_SET:
+        try:
+            payload = json.dumps({
+                "question":   case["question"],
+                "mode":       "direct",
+                "enable_rag": False,
+            }).encode()
+            req = urllib.request.Request(
+                "http://localhost:8000/ask",
+                data=payload,
+                headers={"Content-Type": "application/json"},
+            )
+            with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
+                answer = json.loads(resp.read()).get("answer", "")
+            ok = case["check"](answer)
+            passed += int(ok)
+            results.append({"question": case["question"], "passed": ok})
+        except Exception as exc:  # noqa: BLE001
+            results.append({"question": case["question"], "passed": False, "error": str(exc)})
+
+    return {
+        "total":     len(EVAL_SET),
+        "passed":    passed,
+        "pass_rate": round(passed / len(EVAL_SET), 3),
+        "details":   results,
+    }
+
 # ────────────────────────────────────────────────────────────────────────────
 # CONCEPT · Frontend  [all phases]
 # Serve the single-page UI; every phase of the workshop is driven through it.
```


---

## Show the product was built sequentially

```bash
git diff v0 v4 -- app/main.py     # what the first four steps added, together
git log --oneline v0..v4          # (tags are snapshots, not a linear log)
```

At the end: `git checkout v8` in Clone B to preview everything beyond the core (agents, MCP, safety, evals).
