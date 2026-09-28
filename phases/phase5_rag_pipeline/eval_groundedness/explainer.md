# Evaluating Groundedness: Hallucination Detection & Citation Verification

> **Time:** ~2 min read | **Goal:** Measure whether generated answers faithfully reflect retrieved context or introduce hallucinations.

---

## 1. What is Groundedness?

In a RAG application, an answer is **grounded** (or faithful) if every factual claim it makes is directly supported by the retrieved context.

An answer is **ungrounded (hallucinated)** if:
- It makes claims not present in the provided notes.
- It extrapolates beyond the evidence.
- It contradicts the source text.

---

## 2. The Evaluation Pyramid

To evaluate RAG responses effectively without incurring massive latency or cost, we use a two-tiered evaluation:

### Tier 1: Fast Deterministic Heuristics (`check_length_and_citation`)
- Word count: Does the response stay concise (e.g. $\le 100$ words)?
- Citations: Does it contain citation markers like `[Chunk 1 — bio.md]`?
- Cost: 0 API calls, $\sim 0.01$ milliseconds.

### Tier 2: LLM-as-Judge (`check_groundedness`)
- Passes the context and generated answer to a fast judge model with a strict prompt:
  *"Does the answer contain ONLY information from the context above? YES or NO."*
- Catches subtle hallucinations and extrapolations.

---

## 3. Groundedness in CI/CD

By running groundedness benchmarks automatically on pull requests:
- You detect prompt regressions before deployment.
- You verify that changes to chunk size or retrieval thresholds don't increase hallucination rates.
