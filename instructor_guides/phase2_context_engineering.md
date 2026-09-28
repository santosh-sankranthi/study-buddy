# Phase 2 Instructor Guide: Context Engineering & Memory

The model is stateless. Everything it "remembers" is text *we* put back into the
prompt, and every token we add costs money and latency. Phase 2 is about
choosing what goes in the window.

## 0. Failure demo — run this before you explain anything (5 min)

```bash
python scripts/switch_version.py v1          # persona works, but no memory
uvicorn app.main:app --reload
```

1. Say `My name is Ana and I'm studying for the biology exam.`
2. Then ask `What am I studying for?`
   - It has no idea — v1 sends only the current turn. **That** is the break.
3. Try a long back-and-forth, then keep going: the prompt grows without bound
   until it is expensive, slow, and eventually over the window.

Restore later with `python scripts/switch_version.py v6`.

## Learning objectives

1. Enumerate every source that enters the prompt and measure its tokens.
2. Give the app multi-turn memory via session IDs.
3. Bound that memory with token-budget trimming and summarisation (compaction).
4. Feel the cost/latency wall that motivates keeping context small.
5. Sanitize obvious prompt injection before it reaches the model.

## Timing & pacing (total ~50 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 2.1 Context sources | 2 | 4 | 3 | 1 |
| 2.2 Memory | 2 | 5 | 4 | 1 |
| 2.3 Context compaction | 2 | 5 | 4 | 1 |
| 2.4 Long context | 2 | 4 | 3 | 1 |
| 2.5 Context security | 2 | 3 | 2 | 1 |
| 2.6 MCP (concept) | 3 | — | — | — |

## Live-coding scripts

### 2.1 Context sources — `phases/phase2_context_engineering/context_sources/`

```bash
python phases/phase2_context_engineering/context_sources/demo/main.py
```

Builds a multi-part prompt (system + injected date/name + history + query) and
prints `context_report()`'s per-role token breakdown. Ask the class: "which of
these did the *model* bring, and which did *we* stuff in?" **Twist:** students
add one new source (e.g. the current date) and update the breakdown.

### 2.2 Memory — `phases/phase2_context_engineering/memory/`

```bash
python phases/phase2_context_engineering/memory/demo/main.py
```

Shows `append()` / `get_history()` / `clear()` on a session id, then the app's
`/session/{id}/history` endpoint. **Twist:** students implement a budget based
on the last N **tokens** (not last N turns) — `trim_to_token_budget()` in
`app/memory.py`.

```bash
python phases/phase2_context_engineering/memory/solution/check.py
```

### 2.3 Context compaction — `phases/phase2_context_engineering/context_compaction/`

```bash
python phases/phase2_context_engineering/context_compaction/demo/main.py
```

When history exceeds `COMPACT_BUDGET`, `compact_if_needed()` summarises the
oldest half into one system message and keeps the recent turns. **Twist:**
students implement a *different* strategy — keep the system message + a running
summary + only the **last 2 turns** verbatim (`compact_keep_last2()`), rather
than halving.

### 2.4 Long context — `phases/phase2_context_engineering/long_context/`

```bash
python phases/phase2_context_engineering/long_context/demo/main.py
```

Measures how latency and estimated cost climb as the document grows. Land the
punchline: pasting the whole textbook is slower and pricier than pasting the two
relevant paragraphs. **Twist:** students plot latency/cost in steps to build the
intuition that motivates keeping context small.

### 2.5 Context security (light pass) — `phases/phase2_context_engineering/context_security/`

```bash
python phases/phase2_context_engineering/context_security/demo/main.py
```

`sanitize_input()`/`detect_injection()` strip an obvious "ignore previous
instructions" and replace it with `[BLOCKED]`. This is a shallow pass; Phase 5
goes deep. **Twist:** students add detection for a different phrasing family.

### 2.6 MCP — concept only (no demo/exercise)

Mention it briefly: "MCP is a standard for plugging tools and data into any
model host; we build one in Phase 4." Do not detour.

## Common student mistakes

- **Forgetting the system prompt in the count.** It is re-sent every turn — it
  is *not* free just because it never changes.
- **Trimming by turns when messages vary wildly in size.** A "turn" can be 5 or
  5,000 tokens; trim by tokens.
- **Losing the summary.** Compaction must keep the summary *and* recent turns;
  dropping either loses continuity.
- **Sanitizing only the first message.** Injection can arrive in any turn.
- **Assuming memory is persistent.** It is an in-process dict — it dies with the
  server and is per-session.

## Discussion questions to close

- **What is the difference between "the model remembers" and "we re-sent the
  history"?** There is none — memory is prompt engineering.
- **If compaction summarises history, what can be lost?** Exact wording,
  names, numbers; a summary is lossy. When does that matter for a tutor?
