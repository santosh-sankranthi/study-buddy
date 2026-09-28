"""ChromaDB vector store — persistent note indexing and retrieval.

Grows through the phases:
  Phase 4.1 — index_document(), count()
  Phase 4.2 — search() with optional subject filter
  Phase 5.3 — retrieve() with min_similarity threshold
"""

from __future__ import annotations

import uuid

import chromadb

from app.embeddings import embed

_client     = chromadb.PersistentClient(path="./data/chroma")
_collection = _client.get_or_create_collection(
    name="study_notes",
    # Use cosine distance so higher score = more similar.
    metadata={"hnsw:space": "cosine"},
)


# ── Phase 4.1: Indexing ───────────────────────────────────────────────────────

def index_document(text: str, metadata: dict) -> str:
    """Embed *text* and add it to the collection.

    Args:
        text:     The document text to index.
        metadata: Arbitrary key-value pairs (e.g. {"filename": "...", "subject": "..."}).

    Returns:
        The generated doc_id (UUID string).
    """
    doc_id = str(uuid.uuid4())
    _collection.add(
        ids=[doc_id],
        embeddings=[embed(text)],
        documents=[text],
        metadatas=[metadata],
    )
    return doc_id


def count() -> int:
    """Return the total number of indexed documents."""
    return _collection.count()


# ── Phase 4.2: Similarity search with optional metadata filter ────────────────

def search(
    query: str,
    k: int = 3,
    subject: str | None = None,
) -> list[dict]:
    """Search the collection by semantic similarity.

    Args:
        query:   The search query.
        k:       Number of results to return.
        subject: Optional subject tag filter (e.g. "biology").

    Returns:
        List of {"text", "doc_id", "metadata", "distance"} dicts.
    """
    where = {"subject": subject} if subject else None
    results = _collection.query(
        query_embeddings=[embed(query)],
        n_results=min(k, max(_collection.count(), 1)),
        where=where,
    )
    docs   = results["documents"][0]
    metas  = results["metadatas"][0]
    ids    = results["ids"][0]
    dists  = results["distances"][0]
    return [
        {
            "text":     doc,
            "doc_id":   doc_id,
            "metadata": meta,
            "distance": round(dist, 4),
        }
        for doc, doc_id, meta, dist in zip(docs, ids, metas, dists)
    ]


# ── Phase 5.3: Retrieval with minimum-similarity threshold ───────────────────

def retrieve(
    query: str,
    k: int = 3,
    subject: str | None = None,
    min_similarity: float = 0.3,
) -> list[dict] | None:
    """Search and filter by minimum cosine similarity.

    ChromaDB with cosine space returns distance ∈ [0, 2] where 0 = identical.
    We convert: similarity = 1 - distance.

    Returns:
        Filtered list of results, or None if nothing passes the threshold.
    """
    if _collection.count() == 0:
        return None
    raw = search(query, k=k, subject=subject)
    # distance is in [0,2] for cosine; similarity = 1 - distance
    filtered = [r for r in raw if (1.0 - r["distance"]) >= min_similarity]
    return filtered if filtered else None
