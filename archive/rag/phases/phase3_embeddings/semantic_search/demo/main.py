"""DEMO -- Semantic Search in app/search.py.

Live-code target: execute semantic_search() from app.search over a set of
candidate study notes, showing how conceptual similarity surfaces the correct
note even when lexical words do not overlap.

Run:
    python phases/phase3_embeddings/semantic_search/demo/main.py
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

QUERY = "how do plants make food?"

print("=" * 60)
print(f"SEMANTIC SEARCH DEMO")
print(f"Query: '{QUERY}'")
print("=" * 60)

results = semantic_search(QUERY, DOCS, k=3)

print("\nTop 3 Ranked Results:")
for i, item in enumerate(results, 1):
    print(f"  [{i}] Score: {item['score']:0.4f} | {item['text']}")

print("\nObservation:")
print("Notice the query contains 'plants', 'make', 'food', while the top doc")
print("contains 'autotrophs', 'solar radiation', 'glucose'. Zero keyword overlap,")
print("yet semantic search matched them correctly!")
