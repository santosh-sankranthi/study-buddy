# Phase 4 Instructor Guide: Vector Databases (ChromaDB)

Phase 3 searched an in-memory list. That does not survive a restart and gets
slow as the corpus grows. Phase 4 introduces a real vector store: persistent,
indexed, and filterable.

## 0. Failure demo — run this before you explain anything (3 min)

```bash
python - <<'PY'
from app.search import semantic_search
docs = ["Photosynthesis converts light to energy."] * 3
print("in-memory only:", len(docs), "docs")
try:
    from app.vector_store import count
    print("indexed docs:", count())
except Exception as e:
    print("no persistent store yet:", e)
PY
```

Point out the two problems: the Phase 3 list vanishes when the process exits,
and there is no way to ask "only search my *physics* notes". Chroma solves both.

## Learning objectives

1. Why a vector DB beats an in-memory list (persistence, ANN index, metadata).
2. Index documents with metadata into a persistent Chroma collection.
3. Query top-k by similarity.
4. Constrain a query with a metadata filter.

## Timing & pacing (total ~35 min)

| Concept | Explain | Demo | Exercise | Debrief |
|---|---|---|---|---|
| 4.1 Indexing | 3 | 6 | 5 | 1 |
| 4.2 Similarity search | 3 | 6 | 9 | 2 |

## Live-coding scripts

### 4.1 Indexing — `phases/phase4_vector_databases/indexing/`

```bash
python phases/phase4_vector_databases/indexing/demo/main.py
```

Shows `index_document()` writing into the embedded (no server!) Chroma
collection at `./data/chroma`, then `count()`. Emphasise: embedded mode means
students run **zero infrastructure**. **Twist:** students ingest ~20 docs
instead of 5 and observe it still just works.

```bash
python phases/phase4_vector_databases/indexing/solution/check.py
```

### 4.2 Similarity search — `phases/phase4_vector_databases/similarity_search/`

```bash
python phases/phase4_vector_databases/similarity_search/demo/main.py
```

Runs the same query with and without `where={"subject": "physics"}`, showing how
the filter restricts results to one domain. **Twist:** students add a metadata
filter so a query only searches chunks tagged to a single subject.

## Common student mistakes

- **Reading Chroma's `distance` as similarity.** With cosine space,
  `similarity = 1 - distance`. Identical vectors have distance `0`.
- **Re-indexing on every run.** The store persists; uploading the same notes
  twice duplicates chunks. Clear `data/chroma/` or use fresh metadata if that
  happens.
- **Filtering on metadata you never stored.** The `where` clause only matches
  keys you passed to `index_document()`.
- **`n_results` larger than the collection.** It is clamped internally, but
  students expect more rows than exist.
- **Assuming a server is required.** This is embedded Chroma — there is no
  daemon to start.

## Discussion questions to close

- **When does an in-memory list stop being good enough?** When you need
  persistence, metadata filtering, or sub-linear search over a large corpus.
- **What does the metadata filter guarantee that similarity alone cannot?** That
  a "biology" query never returns a "history" chunk, no matter the scores.
