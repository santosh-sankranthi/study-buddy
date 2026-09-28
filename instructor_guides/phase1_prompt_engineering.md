# Phase 1 Instructor Guide: Prompt Engineering

Phase 1 is where the app stops sounding like a raw model and starts sounding
like a tutor. Every demo is a small script that calls `common.llm.chat()`; the
last step of each wires the same code into `app/` so the running app improves.

## 0. Failure demo — run this before you explain anything (5 min)

```bash
python scripts/switch_version.py v0          # raw one-shot, no persona
uvicorn app.main:app --reload
```

Ask `What is photosynthesis?` twice. The answers are a different shape each
time — wrong length, wrong tone, no consistent voice. That inconsistency is the
whole motivation for a **system prompt**.

When the phase is over, restore the end state: `python scripts/switch_version.py v6`
(or `v1` to see only this phase's app).

## Learning objectives

1. System prompts anchor persona and constraints on every call.
2. Few-shot examples enforce a rigid output format.
3. Chain-of-thought changes *correctness*, not just verbosity.
4. Pydantic turns "usually JSON" into "validated JSON or an exception".
5. Tool schemas are a contract the model can choose to call.
6. ReAct is a reasoning *pattern* — thought → action → observation.

## Timing & pacing (total ~60 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 1.1 System prompts | 2 | 4 | 3 | 1 |
| 1.2 Few-shot / zero-shot | 2 | 4 | 3 | 1 |
| 1.3 CoT | 2 | 4 | 3 | 1 |
| 1.4 Structured output | 2 | 6 | 6 | 1 |
| 1.5 Function calling (concept) | 2 | 4 | 2 | 1 |
| 1.6 ReAct (concept) | 2 | 3 | 2 | 1 |

## Live-coding scripts

### 1.1 System prompts — `phases/phase1_prompt_engineering/system_prompts/`

```bash
python phases/phase1_prompt_engineering/system_prompts/demo/main.py
```

The demo sends one question twice: once raw, once with `TUTOR_SYSTEM_PROMPT`.
Read the two answers aloud. Then open `app/prompts.py` and show
`TUTOR_SYSTEM_PROMPT` — "this is the entire personality, five lines."
**Twist:** students write a strict-JSON flashcard persona instead.

```bash
python phases/phase1_prompt_engineering/system_prompts/solution/check.py
```

### 1.2 Few-shot / zero-shot — `phases/phase1_prompt_engineering/few_shot_zero_shot/`

```bash
python phases/phase1_prompt_engineering/few_shot_zero_shot/demo/main.py
```

Two worked Q→MCQ examples via `build_few_shot_prompt()` make the format stick.
Contrast with the zero-shot call in the same script. **Twist:** students build
few-shot examples that turn a question into a multiple-choice quiz item.

### 1.3 Chain of thought — `phases/phase1_prompt_engineering/cot/`

```bash
python phases/phase1_prompt_engineering/cot/demo/main.py
```

Same logic puzzle with and without "think step by step". Point out that CoT can
flip a *wrong* answer to *right* — it is not just longer. Then show the
`<thinking>` / `<answer>` tag parsing wired into `app/main.py`.
**Twist:** students run the same comparison on a math word problem and report
whether **correctness** changed, not just verbosity.

### 1.4 Structured output — `phases/phase1_prompt_engineering/structured_output/`

```bash
python phases/phase1_prompt_engineering/structured_output/demo/main.py
```

Define `Flashcard(question, answer, difficulty)`, call the model, validate with
`model_validate_json()`. Then **deliberately break it** — drop a required field
and show the `ValidationError`. That red traceback is the lesson: "the model
being *usually* right is not a contract."
**Twist:** students define and validate their own `StudyPlanDay(subject,
topics, minutes)` schema (see `app/schemas.py`).

### 1.5 Function calling (concept only) — `phases/phase1_prompt_engineering/function_calling_concept/`

```bash
python phases/phase1_prompt_engineering/function_calling_concept/demo/main.py
```

Walk the JSON tool schema in `app/tools.py` (`search_notes`,
`get_exam_schedule`, `calculate_grade`). Point out `parameters` / `required`.
This is **schema shape only** — nothing is executed yet (execution returns for
real in Phase 3). **Twist:** students write their own `get_definition(term)`
tool schema.

### 1.6 ReAct (concept only) — `phases/phase1_prompt_engineering/react_concept/`

```bash
python phases/phase1_prompt_engineering/react_concept/demo/main.py
```

Trace `thought → action → observation` on the board. **Twist:** students
hand-trace a different scenario (e.g. "find today's date, then days until an
exam") writing each line by hand — no code. See `exercise/trace.md`.

## Common student mistakes

- **A wall of persona text.** More words is not more control; concrete rules
  ("replies under 4 sentences") beat adjectives.
- **Examples that disagree.** In few-shot, if your two examples format the JSON
  differently, the model averages them into something invalid.
- **CoT on trivial tasks.** Simple lookups don't need reasoning; it just burns
  tokens and time.
- **Schema and prompt drift.** Students change the prompt's JSON shape but not
  the Pydantic model (or vice-versa) → `ValidationError`. Keep them paired.
- **Confusing schema with execution.** In 1.5 the model *proposes* a call; no
  Python runs. That comes in 3.2.

## Discussion questions to close

- **Why can a 5-line system prompt outperform a 2-page one?** Specificity beats
  length; the model follows concrete, checkable rules.
- **When would few-shot be the wrong tool?** When the task is open-ended — rigid
  examples over-constrain creative answers.
