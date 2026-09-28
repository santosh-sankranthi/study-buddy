# Regression Testing: Drift Prevention in CI/CD

> **Time:** ~2 min read | **Goal:** Prevent prompt drift and capability regressions using automated test suites.

---

## 1. The Prompt Engineering Regressions Problem

In traditional software, changing a helper function runs unit tests with deterministic assertions.
In AI engineering:
- You tweak the system prompt to make the model friendlier.
- Suddenly, the model starts failing JSON formatting on `/flashcards`.
- Or you increase temperature to make quiz questions more diverse, and hallucination rates surge.

Without automated **regression testing**, you only discover breakages when end users complain.

---

## 2. Benchmark Datasets (Golden Sets)

A regression test suite maintains a **Golden Set** of representative inputs:
- 10 standard educational questions
- 5 edge cases (empty strings, obscure jargon, multilingual inputs)
- 5 injection attacks
- 5 structured output requests

---

## 3. CI/CD Integration

Every pull request runs the benchmark:
```
Total Test Cases:   25
Deterministic Pass: 25/25 (100%)
Groundedness Pass:  24/25 (96%)
Latency P95:        480ms (Within 600ms budget)
Cost:               $0.012

Verdict: ✅ PASSED (Exceeds 90% threshold)
```

If a prompt change drops the pass rate below the release threshold (e.g. $<90\%$), CI blocks deployment.
