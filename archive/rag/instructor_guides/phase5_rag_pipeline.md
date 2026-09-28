# Phase 5 Instructor Guide: Retrieval-Augmented Generation (RAG)

Phases 3–4 gave us searchable notes. Phase 5 wires search **into generation**:
retrieve the relevant notes, put them in the prompt, and refuse to answer when
they don't cover the question. This is the phase where the app becomes honest.

## 0. Failure demo — run this before you explain anything (5 min)

```bash
python scripts/switch_version.py v3          # search works, /ask is NOT grounded
uvicorn app.main:app --reload
```

Ask something that is only answerable from the student's notes, e.g.
`What does my biology note say about the exam date?` v3 answers confidently from
its training data — it has no idea what is in the notes, and it guesses. That
confident wrongness is exactly what RAG prevents.

Restore later with `python scripts/switch_version.py v8` (or `v4`).

## Learning objectives

1. Chunking strategy changes what can be retrieved (size + overlap).
2. Retrieval needs a confidence floor, not just top-k.
3. A grounded prompt forbids outside knowledge and demands citations.
4. Groundedness can be checked (deterministically, then with an LLM judge).

## Timing & pacing (total ~55 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 5.1 Chunking | 2 | 5 | 5 | 1 |
| 5.2 Embedding (plumbing) | 3 | — | — | — |
| 5.3 Indexing | 2 | 4 | 5 | 1 |
| 5.4 Retrieval | 2 | 5 | 5 | 1 |
| 5.5 Grounded generation | 2 | 5 | 5 | 1 |
| 5.6 RAG evaluation | 2 | 4 | 4 | 1 |

## Live-coding scripts

### 5.1 Chunking — `phases/phase5_rag_pipeline/chunking/`

```bash
python phases/phase5_rag_pipeline/chunking/demo/main.py
```

Shows `chunk_fixed(size=200, overlap=50)`: a sliding window where consecutive
chunks share words so a sentence split across the boundary is still recoverable.
**Twist:** students implement paragraph-based chunking (`chunk_paragraph()`) and
compare retrieval quality against fixed-size on the same query.

### 5.2 Embedding — plumbing, no demo

Say one line: "embeddings and the vector store are reused verbatim from Phases
3–4; we are not rewriting them." Point at `phases/phase5_rag_pipeline/embedding/explainer.md`.

### 5.3 Indexing — `phases/phase5_rag_pipeline/indexing/`

```bash
python phases/phase5_rag_pipeline/indexing/demo/main.py
```

End-to-end: load text → `chunk_fixed()` → attach metadata → `index_document()`.
**Twist:** students ingest a larger set and observe it still just works.

### 5.4 Retrieval — `phases/phase5_rag_pipeline/retrieval/`

```bash
python phases/phase5_rag_pipeline/retrieval/demo/main.py
```

`retrieve(query, k=3, min_similarity=0.3)`: on-topic queries return chunks,
off-topic queries return `None`. Land it: "top-k always returns *something*;
a threshold lets us return *nothing*." **Twist:** students tune the threshold
and measure how many chunks survive at loose / balanced / strict values.

### 5.5 Grounded generation — `phases/phase5_rag_pipeline/grounded_generation/`

```bash
python phases/phase5_rag_pipeline/grounded_generation/demo/main.py
```

`build_rag_prompt()` constructs a system prompt that says: answer **only** from
context, cite `[Chunk N — filename.md]`, and say "I don't have enough
information in your notes" otherwise. Each chunk is wrapped as untrusted data
(`wrap_chunk_as_untrusted`). **Twist:** students write a template variant that
must also cite which chunk/source each answer came from.

### 5.6 RAG evaluation — `phases/phase5_rag_pipeline/eval_groundedness/`

```bash
python phases/phase5_rag_pipeline/eval_groundedness/demo/main.py
```

A yes/no groundedness check (is the answer supported by the retrieved chunk?)
plus a deterministic length/citation check. **Twist:** students write a
different automated check — e.g. "did the answer stay under 100 words" or "did
it include a citation."

## Common student mistakes

- **Chunks too large or too small.** Too large dilutes the embedding and wastes
  context; too small loses the sentence's meaning. Overlap exists to soften it.
- **Skipping the similarity threshold.** Without one, retrieval always returns
  the least-bad chunk and the model answers from noise.
- **Forgetting to re-index after re-chunking.** Old chunks linger in Chroma and
  pollute results.
- **Letting the grounded prompt drift.** If the system prompt stops saying
  "only from context", hallucination comes straight back.
- **Testing groundedness with an exact-string assert.** LLM wording varies —
  check behaviour (citation present, under N words), not text.

## Discussion questions to close

- **When should the app refuse instead of answering?** When retrieval finds
  nothing above threshold — a confident guess is worse than "I don't know."
- **What does a citation buy you?** It makes the answer auditable: a human can
  check the claim against the chunk it came from.
