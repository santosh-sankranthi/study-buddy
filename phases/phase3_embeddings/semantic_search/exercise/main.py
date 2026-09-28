"""EXERCISE -- Query Invariance in Semantic Search.

The demo demonstrated zero-keyword semantic retrieval.
Your twist: verify that semantic search ranking is invariant to query phrasing.
Search across 3 radically different phrasings of the same question and confirm
that all 3 phrasings rank the relevant Biology document at position #1.

Fill in every TODO. Run when done:
    python phases/phase3_embeddings/semantic_search/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.search import semantic_search

DOCS = [
    "Photosynthesis: autotrophs convert solar radiation and carbon dioxide into glucose.",
    "Newton's laws of motion explain inertia, force acceleration, and reactive pairs.",
    "The hydrologic water cycle involves evaporation, transpiration, condensation, and precipitation.",
    "Mitosis is cellular division resulting in two diploid daughter cells identical to the parent.",
    "The French Revolution of 1789 marked the collapse of the monarchy and feudal privileges.",
]

PHRASINGS = [
    "how do plants make food?",
    "what is photosynthesis?",
    "explain how sunlight powers plant growth",
]


# ── TODO(1): Execute semantic search for each phrasing ───────────────────────
def evaluate_phrasings() -> list[str]:
    """Execute semantic_search for each phrasing and return list of top document texts."""
    top_docs = []
    # TODO(1): for each p in PHRASINGS, call semantic_search(p, DOCS, k=1)
    #          and append results[0]['text'] to top_docs
    for p in PHRASINGS:
        res = semantic_search(p, DOCS, k=1)
        top_docs.append(res[0]["text"])
    return top_docs


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Semantic search projects different synonyms and phrasing variations to neighboring "
    "coordinates in the embedding space, ensuring consistent top-1 retrieval."
)


if __name__ == "__main__":
    top = evaluate_phrasings()
    for phrasing, result in zip(PHRASINGS, top):
        print(f"Query: '{phrasing}'")
        print(f"  Top Match: {result}\n")
    print("Observation:", OBSERVATION)
