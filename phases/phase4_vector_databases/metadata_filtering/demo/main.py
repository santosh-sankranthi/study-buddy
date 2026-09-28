"""DEMO -- Metadata Pre-filtering in app/vector_store.py.

Live-code target: execute vector searches with and without subject metadata filters,
observing how pre-filtering guarantees domain-restricted results.

Run:
    python phases/phase4_vector_databases/metadata_filtering/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import index_document, search

print("=" * 60)
print("METADATA FILTERING DEMO")
print("=" * 60)

# Ensure sample documents across different subjects exist
index_document("ATP is the primary biochemical energy currency used in cellular processes.", {"subject": "biology"})
index_document("Kinetic energy is the energy possessed by an object due to its motion: 0.5 * m * v^2.", {"subject": "physics"})

query = "energy and work"

# 1. Unfiltered search
print(f"\nUnfiltered search for: '{query}'")
all_res = search(query, k=2)
for i, r in enumerate(all_res, 1):
    print(f"  [{i}] Subject: {r['metadata'].get('subject')} | {r['text'][:60]}...")

# 2. Filtered search (Physics only)
print(f"\nFiltered search (subject='physics') for: '{query}'")
phys_res = search(query, k=2, subject="physics")
for i, r in enumerate(phys_res, 1):
    print(f"  [{i}] Subject: {r['metadata'].get('subject')} | {r['text'][:60]}...")

# 3. Filtered search (Biology only)
print(f"\nFiltered search (subject='biology') for: '{query}'")
bio_res = search(query, k=2, subject="biology")
for i, r in enumerate(bio_res, 1):
    print(f"  [{i}] Subject: {r['metadata'].get('subject')} | {r['text'][:60]}...")
