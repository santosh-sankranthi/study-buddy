"""EXERCISE -- Strict Metadata Pre-Filtering.

The demo filtered by biology and physics.
Your twist: implement search_subject_only() and assert that when filtering
by a specific subject (e.g. 'chemistry'), every single returned item has
metadata['subject'] == 'chemistry'.

Fill in every TODO. Run when done:
    python phases/phase4_vector_databases/metadata_filtering/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import index_document, search


# ── TODO(1): Setup Chemistry documents ───────────────────────────────────────
def seed_chemistry_notes() -> None:
    """Index two chemistry notes with metadata subject='chemistry'."""
    # TODO(1): index two notes with {"subject": "chemistry"}
    index_document("Covalent bonds involve the mutual sharing of electron pairs between atoms.", {"subject": "chemistry"})
    index_document("Acids are proton donors (Bronsted-Lowry) or electron pair acceptors (Lewis).", {"subject": "chemistry"})


# ── TODO(2): Implement search_subject_only ───────────────────────────────────
def search_subject_only(query: str, subject: str, k: int = 2) -> list[dict]:
    """Execute search(query, k=k, subject=subject) and return the results."""
    # TODO(2): return search(query, k=k, subject=subject)
    return search(query, k=k, subject=subject)


# ── TODO(3): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Pre-filtering restricts the search domain before or during vector ranking, ensuring "
    "100% precision on metadata fields without risk of returning fewer than k results."
)


if __name__ == "__main__":
    seed_chemistry_notes()
    res = search_subject_only("sharing of electrons in bonds", "chemistry", k=2)
    print(f"Retrieved {len(res)} results for subject='chemistry':")
    for r in res:
        print(f"  Subject: {r['metadata'].get('subject')} | {r['text']}")
    print("\nObservation:", OBSERVATION)
