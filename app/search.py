"""Semantic search (Phase 3.3).

Uses embed() + cosine_similarity() from app.embeddings to rank documents.
No vector DB here — that comes in Phase 4 with ChromaDB.
"""

# ──────────────────────────────────────────────────────────────────────────────
# CONCEPT · Semantic search  [Phase 3.3]
# Rank a list of documents by how close their embeddings are to the query --
# no database yet, just embed + cosine similarity.
# Wired into: /semantic-search.
# ──────────────────────────────────────────────────────────────────────────────

from __future__ import annotations

from app.embeddings import cosine_similarity, embed, embed_batch


def semantic_search(query: str, docs: list[str], k: int = 3) -> list[dict]:
    """Rank *docs* by semantic similarity to *query*.

    Args:
        query: The search query string.
        docs:  List of document strings to search over.
        k:     Number of top results to return.

    Returns:
        List of {"text": str, "score": float} dicts, highest score first.
    """
    if not docs:
        return []

    query_vec = embed(query)
    doc_vecs  = embed_batch(docs)

    scored = [
        {"text": doc, "score": round(cosine_similarity(query_vec, vec), 4)}
        for doc, vec in zip(docs, doc_vecs)
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]
