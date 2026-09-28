# Fine-Tuning vs. RAG vs. Prompt Engineering

> **Time:** ~3 min read | **Goal:** Master the architectural decision matrix to select the right approach for any AI engineering problem.

---

## 1. The Three Levers of AI Engineering

When building an LLM application, you have three primary architectural levers:

| Dimension | Prompt Engineering | RAG | Fine-Tuning |
| :--- | :--- | :--- | :--- |
| **Primary Use Case** | Personas, task instructions, few-shot formatting | Dynamic, private, or frequently updating facts | Style, tone, strict syntax, latency/cost reduction |
| **Knowledge Dynamicism** | Low (bounded by prompt size) | **Very High** (instant updates via vector DB) | Low (frozen in weights at training time) |
| **Source Citations** | Difficult (model relies on context or weights) | **Native & Verifiable** | Impossible (no direct attribution) |
| **Latency & Cost** | Linear with context length | Adds retrieval overhead (~10–50ms) | **Lowest** (shorter prompts, smaller models) |
| **Setup Complexity** | Lowest (minutes) | Medium (hours) | Highest (days, dataset curation, GPUs) |

---

## 2. Common Anti-Patterns

1. **"We have 100 internal PDFs, let's fine-tune a model!"**
   - ❌ Anti-pattern: Fine-tuning does not teach reliable facts. The model will hallucinate and cannot cite page numbers. Use **RAG**.
2. **"Our prompt is 8,000 tokens of few-shot examples and costs $50k/month."**
   - ❌ Anti-pattern: Using massive prompts for static style or formatting. Fine-tuning a smaller model (via LoRA/PEFT) bakes the format into weights and eliminates the prompt overhead. Use **Fine-Tuning**.
3. **"We want to test if users like a Socratic tutor persona."**
   - ❌ Anti-pattern: Spending weeks training a model before validating demand. Use **Prompt Engineering**.

---

## 3. Parameter-Efficient Fine-Tuning (PEFT & LoRA)

Traditional full fine-tuning updates all billions of model weights, requiring massive GPU clusters.
**LoRA (Low-Rank Adaptation)** freezes the base weights and trains lightweight low-rank decomposition matrices ($<1\%$ of parameters).
- Drastically reduces memory and compute requirements.
- Allows hot-swapping different task adapters on a single base model.
