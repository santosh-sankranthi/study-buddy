# Phase 5 Instructor Guide: Retrieval-Augmented Generation (RAG)

## Learning Objectives
1. Implement document chunking strategies (fixed size with overlap vs paragraph chunking).
2. Wire vector retrieval into augmented prompt generation.
3. Force explicit source citations (`[Source: filename]`) to combat hallucination.
4. Evaluate groundedness deterministically and via LLM-as-a-judge.

## Timing & Pacing (Total: 55 min)
- **5.1 Chunking (12 min)**: Compare fixed-window vs paragraph chunking.
- **5.2 Embedding (3 min)**: Review plumbing reuse.
- **5.3 Retrieval (15 min)**: Implement threshold guard (`min_similarity`).
- **5.4 Generation (15 min)**: Build grounded prompt template with mandatory citations.
- **5.5 RAG Evaluation (10 min)**: Validate answer groundedness and word limits.
