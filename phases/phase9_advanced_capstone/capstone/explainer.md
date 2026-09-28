# Capstone Project: The Complete AI Engineering System

> **Time:** ~3 min read | **Goal:** Review how every layer of the curriculum integrates into a single, production-grade AI application.

---

## 1. The Architectural Journey

Over 10 phases, we transformed a raw one-shot Q&A script into a robust, secure, production-grade AI platform:

```
┌────────────────────────────────────────────────────────────┐
│                    FastAPI Web Platform                    │
│    (Interactive Chat UI, Mode Switcher, Trace Inspector)   │
└─────────────────────────────┬──────────────────────────────┘
                              │
  ┌───────────────────────────┴───────────────────────────┐
  │                   Security Firewall                   │
  │   - Direct & Indirect Injection Detection (Regex)    │
  │   - PII Scrubbing (Email, Phone, CC)                  │
  │   - Untrusted Data Sandboxing                         │
  │   - Output Moderation Filter                          │
  └───────────────────────────┬───────────────────────────┘
                              │
  ┌───────────────────────────┴───────────────────────────┐
  │                 Context & Memory Layer                │
  │   - Dynamic Metadata Injection (Date, Student Info)   │
  │   - Multi-Turn Session Memory (Sliding Window)        │
  │   - Summarization Compaction (Halving / Keep-Last-2)  │
  │   - Token Accounting & Budget Protection              │
  └───────────────────────────┬───────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
┌───────────────────────────┐         ┌───────────────────────────┐
│     Grounded RAG Stack    │         │     Agentic Tool Loop     │
│ - Chunking (Fixed/Para)   │         │ - ReAct Loop (T-A-O)      │
│ - Embeddings API          │         │ - Tool Registry & Safety  │
│ - ChromaDB Vector Store   │         │ - Multi-Agent Planner     │
│ - Strict Citation Format  │         │ - Model Context Protocol  │
└───────────────────────────┘         └───────────────────────────┘
                              │
  ┌───────────────────────────┴───────────────────────────┐
  │                 Evaluation & CI/CD                    │
  │   - Deterministic Assertions (JSON, Schema, Limits)   │
  │   - LLM-as-a-Judge Rubrics                            │
  │   - Groundedness / Faithfulness Verification          │
  │   - Automated Regression Testing Gates                │
  └───────────────────────────────────────────────────────┘
```

---

## 2. Production Checklist

Before shipping an AI engineering application to production, verify:
1. **Determinism:** Structured JSON responses validated by Pydantic.
2. **Security:** Untrusted inputs sanitized and boundaries isolated.
3. **Observability:** Token counts, stage latencies, and execution traces logged.
4. **Safety:** Hard ceilings on agent steps and automated loop detection.
5. **Quality Assurance:** CI regression suite testing prompt stability.
