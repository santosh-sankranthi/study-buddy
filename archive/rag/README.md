# Archived: the RAG / retrieval stack

This folder parks the retrieval part of the workshop, which was removed to keep
the workshop focused. **Nothing here is deleted** — it is just no longer part of
the version ladder, the phase curriculum, or the running app.

What was removed (old phase / version numbering):

| Old | Content |
|-----|---------|
| Phase 3 | Embeddings (vector representations, embedding models, semantic search) |
| Phase 4 | Vector databases (ChromaDB indexing, similarity search) |
| Phase 5 | RAG (chunking, indexing, retrieval, grounded generation, groundedness eval) |
| Phase 8.1 | `rag_isolation` safety concept (untrusted-context fencing) |
| `app/` | `rag.py`, `embeddings.py`, `search.py`, `vector_store.py`, `chunker.py` |
| `app/evals/` | full `groundedness.py` (only `llm_judge` survives in the app) |

## If you want it back

The `rag` code depends on `chromadb` and an embeddings endpoint. To restore:

1. Move the files under `archive/rag/app/` back into `app/`.
2. Move the phase folders under `archive/rag/phases/` back into `phases/` and
   renumber them.
3. Re-add the `/embed`, `/similarity-demo`, `/semantic-search`, `/notes/upload`
   and `/notes/search` endpoints to the composer, plus the RAG block in `/ask`.

The original code is intact and was working; this is a deliberate scope cut, not
a broken extraction.
