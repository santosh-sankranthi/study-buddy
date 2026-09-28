# Phase 3 Instructor Guide: Embeddings & Vector Semantics

Words alone are a terrible index. "Plants absorb sunlight" and "photosynthesis"
share no vocabulary, so keyword search misses the match. Embeddings fix that by
turning meaning into geometry.

## 0. Failure demo — run this before you explain anything (5 min)

Show exact-text search failing.

```bash
python - <<'PY'
notes = {
    "photosynthesis.md": "Plants absorb sunlight to make food.",
    "newtons_laws.md":   "Force equals mass times acceleration.",
}
query = "How do plants make energy?"
hits = [k for k, v in notes.items() if query.lower() in v.lower()]
print("keyword matches:", hits)   # []  <-- no words overlap
PY
```

The word "plants" is the only overlap and it still misses. Land it: exact text
matching cannot answer a question phrased differently from the notes.

## Learning objectives

1. Embeddings map text to high-dimensional vectors where closeness = meaning.
2. Cosine similarity measures the angle between vectors (hand-rolled first).
3. Real `embed()` calls replace toy vectors with 1,536-dimensional ones.
4. Semantic search ranks a document set by similarity to a query.

## Timing & pacing (total ~45 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 3.1 Vector representations | 3 | 6 | 5 | 1 |
| 3.2 Embedding models | 3 | 5 | 5 | 1 |
| 3.3 Semantic search | 2 | 5 | 5 | 1 |

## Live-coding scripts

### 3.1 Vector representations — `phases/phase3_embeddings/vector_representations/`

```bash
python phases/phase3_embeddings/vector_representations/demo/main.py
```

Opens `app/embeddings.py` and shows `cosine_similarity()` built from scratch —
dot product over the product of norms — then ranks 3-D toy vectors. No libraries:
the point is that similarity is just arithmetic. **Twist:** students add a 6th
*adversarial* sentence (similar wording, opposite meaning) and check whether
naive similarity is fooled.

### 3.2 Embedding models — `phases/phase3_embeddings/embedding_models/`

```bash
python phases/phase3_embeddings/embedding_models/demo/main.py
```

Swaps the hand-built vectors for real `embed()` / `embed_batch()` calls and
prints the vector dimension. **Twist:** compare two embedding models on the same
sentence set if a second free one is available, otherwise compare
embedding-based similarity against naive word-overlap similarity.

### 3.3 Semantic search — `phases/phase3_embeddings/semantic_search/`

```bash
python phases/phase3_embeddings/semantic_search/demo/main.py
```

`semantic_search(query, docs, k)` says `search_notes`-style lookup should surface
the right note despite zero word overlap. **Twist:** students build semantic
search over 5 sentences on their own topic and sanity-check the ranking.

```bash
python phases/phase3_embeddings/semantic_search/solution/check.py
```

## Common student mistakes

- **Confusing distance and similarity.** Cosine similarity is `[-1, 1]`; higher
  is closer. Chroma reports *distance* (Phase 4) — do not mix them up.
- **Not normalising.** Cosine handles magnitude for you, which is why we use it
  rather than raw dot product.
- **Expecting rank order to be obvious.** Near-duplicates can swap places; the
  check asserts the *expected doc is in top-k*, not its exact score.
- **Embedding the query with a different model than the docs.** Dimensions and
  spaces must match.
- **Rate limits.** Batch your embeds (`embed_batch`); do not loop one-by-one.

## Discussion questions to close

- **Why is ~1,536 dimensions okay when 3 is enough for the toy demo?** Real
  language needs many independent axes; the toy vectors only encode 3 topics.
- **What kinds of meaning still get lost?** Negation, sarcasm, and rare jargon —
  which is why we add a similarity threshold later.
