"""EXERCISE -- Indexing and Querying with ChromaDB.

The demo indexed biology and physics notes.
Your twist: index two notes on Computer Science, verify that count() increments,
run a search query, and convert ChromaDB distance to cosine similarity.

Fill in every TODO. Run when done:
    python phases/phase4_vector_databases/vector_db_basics/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import count, index_document, search

CS_NOTES = [
    (
        "Binary search operates on a sorted array by repeatedly dividing the search interval in half. O(log n) time.",
        {"filename": "cs_algorithms.md", "subject": "cs"},
    ),
    (
        "Quicksort is an efficient, general-purpose divide-and-conquer comparison sorting algorithm. Average O(n log n).",
        {"filename": "cs_sorting.md", "subject": "cs"},
    ),
]


# ── TODO(1): Index notes into vector store ───────────────────────────────────
def index_cs_notes() -> list[str]:
    """Index both notes from CS_NOTES and return the list of generated doc_ids."""
    doc_ids = []
    # TODO(1): for text, meta in CS_NOTES: call index_document(text, meta)
    for text, meta in CS_NOTES:
        d_id = index_document(text, meta)
        doc_ids.append(d_id)
    return doc_ids


# ── TODO(2): Search and compute similarity ───────────────────────────────────
def search_and_compute_similarity(query: str = "divide and conquer sort") -> list[dict]:
    """Search collection and add 'similarity' field (1.0 - distance) to each result."""
    results = search(query, k=2)
    # TODO(2): for each item in results, compute item['similarity'] = round(1.0 - item['distance'], 4)
    for r in results:
        r["similarity"] = round(1.0 - r["distance"], 4)
    return results


if __name__ == "__main__":
    before = count()
    print("Count before:", before)
    ids = index_cs_notes()
    print("Indexed IDs:", ids)
    print("Count after: ", count())
    res = search_and_compute_similarity("divide and conquer sort")
    for r in res:
        print(f"Similarity: {r['similarity']} | Subject: {r['metadata'].get('subject')} | {r['text'][:60]}...")
