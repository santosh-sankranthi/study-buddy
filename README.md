# Study Buddy — an AI Engineering Workshop

This is a **teaching repo**, not a finished app. It contains one small product
(`app/`) plus a sequence of numbered increments under `phases/`. Each increment
introduces exactly one AI-engineering concept using the same three-beat pattern:

1. **explain** it (2 minutes, `explainer.md`),
2. **live-code** the plainest version of it (`demo/`),
3. **hand students a twist** on the same idea in a different scenario (`exercise/`)
   with a reference answer and self-check (`solution/`).

The product itself grows every phase. The version ladder is:

| Tag | Capability |
|-----|------------|
| `v0` | raw one-shot Q&A (deliberately unimpressive) |
| `v1` | Phase 1 — persona, formats, reasoning (prompt engineering) |
| `v2` | Phase 2 — multi-turn memory + context compaction |
| `v3` | Phases 3+4 — embeddings + vector database |
| `v4` | Phase 5 — RAG grounded in the student's own notes |
| `v5` | Phase 6 — agents (tools + loops) |
| `v6` | Phase 7 — MCP |
| `v7` | Phase 8 — AI safety |
| `v8` | Phase 9 — evaluation + observability |

Do not look at `v8` first. The whole point is that each capability is a *fix*
for something that visibly breaks in the version before it.

## 1. Prerequisites

- Python 3.11+ (3.12 recommended) and a virtualenv.
- An [OpenRouter](https://openrouter.ai) API key — free tier, no card required.
- Git (the workshop is driven with `git checkout` and `git diff` between tags).

## 2. Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and paste your key: OPENROUTER_API_KEY=sk-or-...
```

### Verify the key works before anything else

```bash
python scripts/smoke_test.py
```

That script sends one message to OpenRouter and prints the reply. If it fails,
nothing downstream will work — fix it first.

## 3. Run the app

```bash
uvicorn app.main:app --reload
# open http://127.0.0.1:8000
```

The frontend is one static HTML file (`app/static/index.html`) that `fetch()`es
the FastAPI backend. No build step, no framework — on purpose.

## 4. Run a phase's demo / exercise

Every demo and exercise is a plain script. Run it from the repo root (the
scripts add the repo root to `sys.path` for you, so `python <path>` works):

```bash
python phases/phase0_fundamentals/tokens/demo/main.py

# self-check an exercise after you've filled in its TODOs:
python phases/phase0_fundamentals/tokens/solution/check.py

# check the reference solution instead:
python phases/phase0_fundamentals/tokens/solution/check.py --solution
```

## 5. How the git tagging works

Each concept is committed three times, so the instructor can `git diff` any two
tags live and the diff *is* the lesson:

```bash
git tag                                   # list everything
git diff p1-system-prompts-exercise p1-system-prompts-solution
```

- `p<phase>-<concept>-exercise` — the skeleton students check out to start.
- `p<phase>-<concept>-demo`     — the instructor's live-coded demo, added on top.
- `p<phase>-<concept>-solution` — the reference solution, added on top.

Phase end states are tagged `v0`, `v1`, … `v8`.

## 6. Model configuration

`.env` controls everything:

```
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=openrouter/free
```

`openrouter/free` is a router that auto-selects a free model with whatever
capability the call needs (tool calling, JSON, vision), so we never hardcode a
single free model that might disappear. Free model IDs rotate; see
<https://openrouter.ai/models> filtered by *prompt price: free* for what is
live, and pin the current ones in `OPENROUTER_FALLBACK_MODELS` (comma separated)
in case the router has an off day.

Free tier is roughly 20 requests/minute plus a daily cap. All LLM calls go
through `common/llm.py`, which retries with exponential backoff on rate limits
and falls back across the model list, so a rate-limit blip during a live class
does not kill the demo.

## 7. Repo layout & Curriculum Map

```
study-buddy/
├── app/                 # The live FastAPI product (v0..v8)
│   ├── main.py          # Unified FastAPI backend with all endpoints
│   ├── prompts.py       # Personas, few-shot builders, system prompts
│   ├── schemas.py       # Pydantic schemas (Flashcard, StudyPlanDay, QuizItem)
│   ├── tools.py         # Tool schemas and execution registry (search, schedule, grade)
│   ├── memory.py        # Session history, sliding window, compaction
│   ├── context.py       # Context token breakdown & metadata injection
│   ├── security.py      # Prompt injection detection, PII scrubbing, output moderation
│   ├── chunker.py       # Fixed-size and paragraph chunkers
│   ├── embeddings.py    # Cosine similarity math + embeddings API batching
│   ├── search.py        # Semantic search
│   ├── vector_store.py  # ChromaDB persistent collection
│   ├── rag.py           # Grounded RAG prompt construction & citations
│   ├── agent.py         # Autonomous ReAct loop, safety caps, multi-agent planner
│   ├── evals/           # Groundedness and LLM-as-a-judge evaluators
│   └── static/          # Single-file HTML/CSS/JS interactive frontend
├── common/              # Shared client: llm.chat() + token counting
├── data/sample_notes/   # 13 sample study notes across Biology, Physics, CS
├── mcp_server/          # Standard Model Context Protocol (MCP) server
├── scripts/             # smoke_test.py, tag_phases.sh
└── phases/
    ├── phase0_fundamentals/       (tokens, context_window, training_vs_inference, sampling)
    ├── phase1_prompt_engineering/ (system_prompts, few_shot, cot, structured_output, function_calling, react)
    ├── phase2_context_engineering/ (context_injection, session_memory, context_compaction, long_context, prompt_injection)
    ├── phase3_embeddings/          (vector_math, embedding_api, semantic_search)
    ├── phase4_vector_databases/    (vector_db_basics, metadata_filtering)
    ├── phase5_rag_pipeline/        (chunking, indexing, retrieval, grounded_generation, eval_groundedness)
    ├── phase6_agents_and_tools/    (function_calling_live, react_loop, agent_safety, multi_agent)
    ├── phase7_production_evals/    (latency_cost, evals_deterministic, llm_as_judge, regression_testing)
    ├── phase8_security_safety/     (prompt_injection_advanced, pii_scrubbing, rag_isolation, output_moderation)
    └── phase9_advanced_capstone/   (fine_tuning_concepts, multimodal, eval_frameworks, capstone)
```

## 8. Available API Endpoints

| Endpoint | Method | Phase | Purpose |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | All | Interactive browser application |
| `/ask` | `POST` | 0–5 | Core study buddy Q&A with mode, memory, RAG, and CoT |
| `/modes` | `GET` | 1 | List available tutor personas |
| `/quiz-item` | `POST` | 1.2 | Few-shot generated multiple-choice quiz questions |
| `/flashcards` | `POST` | 1.4 | Validated Pydantic Flashcard generation |
| `/study-plan` | `POST` | 1.4 | Structured multi-day study schedule |
| `/tools` | `GET` | 1.5 | List registered tool JSON schemas |
| `/context-report`| `POST` | 2.1 | Token usage breakdown across prompt roles |
| `/session/{id}/history` | `GET` | 2.2 | Retrieve full conversation memory for a session |
| `/session/{id}` | `DELETE`| 2.2 | Clear session memory |
| `/measure-long-context` | `POST` | 2.4 | Latency & cost benchmarking for expanding token windows |
| `/similarity-demo` | `GET` | 3.1 | Offline vector cosine similarity ranking demo |
| `/embed` | `POST` | 3.2 | Generate vector embeddings for input text |
| `/semantic-search` | `POST` | 3.3 | Pure semantic search ranking over candidate docs |
| `/notes/upload` | `POST` | 4–5 | Upload, chunk, and index study notes into ChromaDB |
| `/notes/search` | `POST` | 4–5 | Semantic search over indexed notes with metadata filtering |
| `/eval/groundedness-report` | `GET` | 5.5 | Groundedness and citation audit log |
| `/agent/ask` | `POST` | 6.2 | Autonomous ReAct agent loop with execution trace |
| `/agent/plan-and-execute` | `POST` | 6.5 | Multi-agent Planner $\rightarrow$ Executor $\rightarrow$ Critic pipeline |
| `/eval/regression-report` | `GET` | 7.4 | Automated regression benchmark report |

## 9. Running the Model Context Protocol (MCP) Server

Study Buddy includes an MCP server wrapping the tools (`search_notes`, `get_exam_schedule`, `calculate_grade`):

```bash
python mcp_server/server.py
```

Configure in Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "study-buddy": {
      "command": "python",
      "args": ["/path/to/study-buddy/mcp_server/server.py"]
    }
  }
}
```

