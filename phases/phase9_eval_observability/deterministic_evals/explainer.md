# Deterministic Evaluations

> **Time:** ~2 min read | **Goal:** Build fast, free, zero-API-call test suites that catch 80% of prompt regressions before running expensive model judges.

---

## 1. Why Not Use LLM Judges for Everything?

Using an LLM to evaluate every single test case:
- Costs money on every test run.
- Adds seconds or minutes of test suite latency.
- Can be non-deterministic itself.

**Deterministic evaluations** run in sub-millisecond Python:
1. Did the response parse as valid JSON?
2. Did it match the Pydantic schema?
3. Did it respect length constraints (e.g. $\le 100$ words)?
4. Did it avoid forbidden phrases (e.g. "as an AI", markdown fences when raw JSON was requested)?
5. Did it contain required fields (citations, sources)?

---

## 2. The Deterministic Test Harness

A typical deterministic test verifies multiple assertions across a candidate string:

```python
def eval_flashcard_response(raw_text: str) -> dict[str, bool]:
    return {
        "valid_json": is_json(raw_text),
        "has_question": bool(data.get("question")),
        "valid_difficulty": data.get("difficulty") in {"easy", "medium", "hard"},
        "under_word_limit": len(raw_text.split()) <= 50,
    }
```

Only if all deterministic gates pass do we proceed to semantic/qualitative checks.
