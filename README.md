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

## 7. Repo layout

```
study-buddy/
├── app/                 # the live product (v0..v8)
├── common/              # shared client: llm.chat() + token counting
├── data/sample_notes/   # short docs used by the RAG phases
├── phases/              # phase<N>_<name>/<concept>/{explainer,demo,exercise,solution}
└── instructor_guides/   # per-phase run-of-show for the instructor
```
