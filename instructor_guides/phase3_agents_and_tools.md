# Phase 3 Instructor Guide: AI Agents & Autonomous Loops

A chatbot answers. An agent *acts*: it picks a tool, runs it, reads the result,
and loops until the job is done — with hard stops so it cannot run forever.
Phase 3 is the biggest jump in the workshop; budget the most time here.

## 0. Failure demo — run this before you explain anything (5 min)

```bash
python scripts/switch_version.py v2          # memory works, but no tools/loops
uvicorn app.main:app --reload
```

Ask `When is my biology exam?` v4 has the exam schedule in `app/tools.py` but
no way to *call* it, so the model invents a plausible date. Then ask a two-part
question (`What's on the biology exam and how many days do I have to study?`) —
v4 can only produce a single answer, no planning, no steps.

Restore later with `python scripts/switch_version.py v6` (or `v3`).

## Learning objectives

1. A tool is a JSON schema plus a real Python function.
2. Function calling = the model *proposes* a call; your code executes it.
3. ReAct = interleaved thought → action → observation.
4. An agent loop needs a stop condition (`MAX_STEPS`) **and** loop detection.
5. Multi-agent = specialist roles passing messages (planner → executor → critic).

## Timing & pacing (total ~60 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 3.1 Tools | 2 | 4 | 3 | 1 |
| 3.2 Function calling (live) | 2 | 4 | 4 | 1 |
| 3.3 ReAct loop | 3 | 5 | 5 | 2 |
| 3.4 Agent loops | 2 | 4 | 5 | 2 |
| 3.5 Agent safety | 2 | 3 | 3 | 1 |
| 3.6 Multi-agent | 3 | 4 | 4 | 2 |

## Live-coding scripts

### 3.1 Tools — `phases/phase3_agents_and_tools/tools/`

```bash
python phases/phase3_agents_and_tools/tools/demo/main.py
```

`app/tools.py` now holds **real** implementations plus `TOOL_REGISTRY`, the
name→function dispatcher. **Twist:** students define a 3rd tool of their own
choosing (schema + function).

### 3.2 Function calling, wired — `phases/phase3_agents_and_tools/function_calling_live/`

```bash
python phases/phase3_agents_and_tools/function_calling_live/demo/main.py
```

`execute_tool_call()` parses `function.arguments` as JSON and dispatches through
`TOOL_REGISTRY`, returning the result to the model. Show the failure path too:
an unknown tool name returns a helpful error instead of crashing.
**Twist:** students wire their own Phase-1/6 tool into the dispatcher.

### 3.3 ReAct loop — `phases/phase3_agents_and_tools/react_loop/`

```bash
python phases/phase3_agents_and_tools/react_loop/demo/main.py
```

Runs `agent_loop()` (in `app/agent.py`) on a real question and prints the
accumulated `trace`. Read the trace aloud: thought, action, observation, repeat.
The app endpoint is `POST /agent/ask`. **Twist:** students extend it to a
question needing **two sequential** tool calls and trace both.

### 3.4 Agent loops — `phases/phase3_agents_and_tools/agent_loops/`

```bash
python phases/phase3_agents_and_tools/agent_loops/demo/main.py
```

A `for step in range(MAX_STEPS)` loop that halts on `done`, on a repeated
tool+args (loop detection), or on the cap — returning a `reason` either way.
**Twist:** students add a different stop condition, e.g. halt if the same tool
is called twice in a row (in addition to the cap).

```bash
python phases/phase3_agents_and_tools/agent_loops/solution/check.py
```

### 3.5 Agent safety — `phases/phase3_agents_and_tools/agent_safety/`

```bash
python phases/phase3_agents_and_tools/agent_safety/demo/main.py
```

Shows a thrashing action stream being caught by loop detection *before* the step
cap is exhausted. Tie it to cost: a runaway loop is a runaway bill.

### 3.6 Multi-agent — `phases/phase3_agents_and_tools/multi_agent/`

```bash
python phases/phase3_agents_and_tools/multi_agent/demo/main.py
```

`plan_and_execute()` runs `planner()` → `executor()` → `critic()` (endpoint
`POST /agent/plan-and-execute`). **Twist:** students add a third role — a critic
that must approve the executor's output before it is returned to the user.

## Common student mistakes

- **Schema/function name mismatch.** The model calls `search_notes`; if the
  registry key differs, dispatch fails. Keep names identical.
- **Arguments that don't parse.** Tool arguments arrive as a JSON *string* —
  always `json.loads` before calling.
- **No iteration cap.** A model that keeps calling the same tool will loop
  forever and spend real money. Cap **and** detect repeats.
- **Confusing ReAct with a fixed pipeline.** ReAct decides at runtime; a
  pipeline is hard-coded.
- **Multi-agent = more cost.** Each role is another LLM call; only add one when
  a single agent demonstrably fails.
- **Streaming/None content.** A tool-call response has `content=None`; read
  `tool_calls`, not `.content`.

## Discussion questions to close

- **What is the real danger of an agent loop with no cap?** Unbounded cost and
  latency, plus side effects from repeated tool calls.
- **Would you add a critic to every pipeline?** Probably not — it doubles calls.
  When is the extra cost worth it?
