# Latency & Cost Profiling in Production

> **Time:** ~2 min read | **Goal:** Measure request latency breakdowns and establish cost accounting for production LLM systems.

---

## 1. Where Does the Time Go?

A common developer mistake is assuming all delay is "the model being slow". In reality, an end-to-end request involves:
1. **Network Overhead:** DNS resolution, TLS handshake to API gateways (~100–250ms).
2. **Embedding Latency:** Forward pass for query embedding (~50–150ms).
3. **Vector Database Retrieval:** HNSW index traversal and document fetching (~5–20ms).
4. **Time to First Token (TTFT):** The model processing prompt tokens before streaming (~300–800ms).
5. **Generation / Decoding:** Sampling tokens iteratively (~20–40ms per output token).

Profiling each stage separately reveals where optimization efforts actually pay off.

---

## 2. Unit Economics: Cost per User Session

When running an application at scale:
$$\text{Cost} = \left(\frac{\text{Input Tokens}}{1,000,000} \times P_{\text{in}}\right) + \left(\frac{\text{Output Tokens}}{1,000,000} \times P_{\text{out}}\right)$$

Cost optimization levers:
- **Prompt trimming & compaction:** Reduces input tokens.
- **Max tokens ceilings:** Limits runaway model verbosity.
- **Smaller/distilled models for intermediate steps:** Use fast, cheap models for classification and routing; reserve frontier models for final synthesis.
