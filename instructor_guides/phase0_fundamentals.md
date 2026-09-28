# Phase 0 Instructor Guide: AI & LLM Fundamentals

Phase 0 changes no code — it builds the mental model every later phase assumes.
Keep it hands-on and fast; resist the urge to lecture.

## 0. Failure demo — run this before you explain anything (5 min)

Put the *unimproved* app in front of the class first.

```bash
python scripts/switch_version.py v0          # raw one-shot Q&A
uvicorn app.main:app --reload                # open http://127.0.0.1:8000
```

1. Ask `What is photosynthesis?` — then ask it **again**.
   - The two answers differ in tone, length and structure. There is no "Study
     Buddy", just a raw model guessing. (Motivates Phase 1's system prompt.)
2. Paste a ~5-page lecture transcript and ask a question.
   - Watch it truncate / error once the prompt exceeds the window.
     (Motivates Phase 2's context engineering.)
3. Ask the same question at temperature extremes (see the sampling demo).
   - Same prompt, different answer every time. (Motivates Sampling.)

Restore the full app when done: `python scripts/switch_version.py v6`.

## Learning objectives

1. Models tokenize text into integer IDs, not words or characters.
2. The context window is a hard limit on input **plus** output tokens.
3. Sampling knobs (temperature, top_p) reshape the probability distribution.
4. Inference is stateless; in-context learning is not training.

## Timing & pacing (total ~45 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 0.1 Tokens | 2 | 4 | 4 | 2 |
| 0.2 Context windows | 2 | 5 | 8 | 2 |
| 0.3 Training vs inference | — | discussion | — | 8 |
| 0.4 Sampling | 3 | 4 | 5 | 2 |

## Live-coding scripts

### 0.1 Tokens — `phases/phase0_fundamentals/tokens/`

```bash
python phases/phase0_fundamentals/tokens/demo/main.py
```

Narrate while it runs: "The model never sees the letters `p-h-o-t-o`. It sees a
list of integers. `tiktoken` lets us peek at that list." Point out that a
'word' and a 'token' are not the same thing — long or unusual words split into
several tokens. **Exercise twist:** students pick their own paragraph and count
it under `cl100k_base` and `o200k_base`, then explain the difference in one
sentence.

```bash
python phases/phase0_fundamentals/tokens/exercise/main.py
python phases/phase0_fundamentals/tokens/solution/check.py            # their work
python phases/phase0_fundamentals/tokens/solution/check.py --solution # reference
```

### 0.2 Context windows — `phases/phase0_fundamentals/context_window/`

```bash
python phases/phase0_fundamentals/context_window/demo/main.py
python phases/phase0_fundamentals/context_window/demo/main.py --live   # real provider error
```

Offline by default (fast, repeatable): it simulates a tiny window and shows the
request crossing the line. `--live` sends an over-budget request and shows the
provider's real error. Land the point: the window is a **budget**, not a
suggestion. **Exercise twist:** given a token budget, calculate how many words
of notes fit alongside a system prompt and 5 turns of history.

### 0.3 Training vs inference — discussion only

There is no demo dir for this concept. Walk the table in
`phases/phase0_fundamentals/training_vs_inference/explainer.md`, then ask the
questions below.

### 0.4 Sampling — `phases/phase0_fundamentals/sampling/`

```bash
python phases/phase0_fundamentals/sampling/demo/main.py
```

Runs the same prompt at temperature `0` and `1.2`, three times each. At `0` the
answers converge; at `1.2` they diverge. **Exercise twist:** repeat the
experiment varying `top_p` instead, and report the behavioural difference.

## Common student mistakes

- **"Tokens = words."** Have them count a sentence with `count_tokens()` and
  compare to `len(text.split())`.
- **"The window is per-message."** It is the sum of system + history + user +
  the model's own reply.
- **"Temperature 0 = deterministic."** It is *greedy*, not guaranteed identical
  across providers/versions.
- **Rate limits:** running the sampling demo in a tight loop can trip the free
  tier's ~20 req/min. `common/llm.py` backs off automatically; tell them a stall
  is the retry wrapper, not a hang.

## Discussion questions to close

- **If you tell Study Buddy something wrong five times, has it learned that?**
  No — weights are frozen at inference. It only sees the errors as tokens in
  the current prompt. Clear the session and it reverts.
- **What would permanently change the model's behaviour?** Fine-tuning via
  gradient descent (or a new pre-training/RLHF run) — expensive, offline, and
  rarely the right first answer (curating the prompt is cheaper and faster).
