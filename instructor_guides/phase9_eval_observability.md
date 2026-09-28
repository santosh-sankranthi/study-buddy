# Phase 9 Instructor Guide: Evaluation & Observability

The app works. The last question is: **how do you know a change made it better
and not just different?** Phase 9 adds a test suite for behaviour, an
LLM-as-judge for open-ended quality, and per-request cost/latency visibility.

## 0. Failure demo — run this before you explain anything (5 min)

```bash
python scripts/switch_version.py v7          # everything works, nothing measured
grep -c "def test" -r app/ || echo "no tests in app/"
uvicorn app.main:app --reload
```

Make a small prompt change (e.g. tweak `TUTOR_SYSTEM_PROMPT`), then answer a
question. It *looks* fine. But: did it get better? Worse? How slow? How much did
that request cost? Nothing in v7 can tell you. That blindness is what Phase 9
fixes.

There is no version past v8 — this is where the ladder ends.

## Learning objectives

1. Deterministic checks catch schema/format regressions for free.
2. LLM-as-a-judge scores open-ended quality (tone, helpfulness, groundedness).
3. Human rubrics calibrate the fuzzy dimensions.
4. Regression runs diff pass-rate before/after a prompt change.
5. Tracing attributes latency and cost to individual pipeline steps.
6. Production monitoring turns those signals into alert rules.

## Timing & pacing (total ~55 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 9.1 Deterministic evals | 2 | 4 | 4 | 1 |
| 9.2 Model-based evals | 3 | 5 | 4 | 1 |
| 9.3 Human evals | 3 | — | 5 | 2 |
| 9.4 Metrics / regression | 2 | 4 | 4 | 1 |
| 9.5 Tracing / cost / latency | 2 | 5 | 4 | 1 |
| 9.6 Production monitoring | 3 | — | 3 | 3 |

## Live-coding scripts

### 9.1 Deterministic evals — `phases/phase9_eval_observability/deterministic_evals/`

```bash
python phases/phase9_eval_observability/deterministic_evals/demo/main.py
```

Zero-cost assertions: JSON parses, schema validates, length bounds, banned
phrases. Emphasise: these run in milliseconds and never flake.
**Twist:** students write a deterministic check for a different field of the
same schema.

### 9.2 Model-based evals — `phases/phase9_eval_observability/model_based_evals/`

```bash
python phases/phase9_eval_observability/model_based_evals/demo/main.py
```

Generalise the Phase-5 groundedness judge into a reusable `llm_judge(answer,
context, criteria)` that returns `{"score": 1-5, "reason": ...}`.
**Twist:** students write a judge prompt scoring **tone/helpfulness** instead of
groundedness.

### 9.3 Human evals — discussion + exercise (no demo)

As a group, score 5 sample outputs against a 3-criteria rubric (see
`phases/phase9_eval_observability/human_evals/exercise/human_eval_rubric.md`).
**Twist:** students design their own 3-criteria rubric and score a different set
of 5 outputs individually.

### 9.4 Metrics / regression — `phases/phase9_eval_observability/metrics_regression/`

```bash
python phases/phase9_eval_observability/metrics_regression/demo/main.py
```

Runs a small eval set and reports a pass rate (release gate: 90%). The app
exposes `GET /eval/groundedness-report` and `GET /eval/regression-report`.
**Twist:** students make their own small prompt tweak, rerun the same eval set,
and report whether it regressed or improved.

### 9.5 Tracing / cost / latency — `phases/phase9_eval_observability/tracing/`

```bash
python phases/phase9_eval_observability/tracing/demo/main.py
```

Profile the pipeline stages (retrieval vs generation), measure milliseconds, and
compute per-step token/cost. **Twist:** students read a trace and identify the
most expensive/slowest step, then propose one concrete fix (cache it, swap to a
cheaper model, reduce `k`).

### 9.6 Production monitoring — discussion + exercise (no demo)

No demo. Discuss what you would alert on if this shipped. **Twist:** students
write 3 concrete alert rules (metric, threshold, why) — see
`phases/phase9_eval_observability/production_monitoring/exercise/alert_rules.md`.

## Common student mistakes

- **Asserting exact LLM wording.** Non-deterministic; assert on shape and
  behaviour instead.
- **A judge with no rubric.** "Is this good?" is meaningless; give criteria and
  a 1–5 scale.
- **Trusting a single eval run.** LLM output varies; run a set and look at the
  pass *rate*.
- **Confusing latency with cost.** A fast call can still be expensive (many
  tokens); a slow one can be cheap. Track both.
- **Alerting on everything.** Too many alerts = ignored alerts. Pick metrics
  that map to user pain (p99 latency, cost/session, groundedness rate).

## Discussion questions to close

- **What would you alert on first if Study Buddy shipped tomorrow?** Cost per
  session, p99 latency, and groundedness/hallucination rate are good answers.
- **When is an LLM judge the wrong tool?** When the property is checkable
  deterministically — do not pay a model to count words.
