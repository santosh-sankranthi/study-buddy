"""DEMO -- Persistent Vector Storage with ChromaDB.

Live-code target: index documents with metadata into ChromaDB using
app.vector_store, inspect collection count, and perform persistent vector search.

Run:
    python phases/phase4_vector_databases/vector_db_basics/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import count, index_document, search

print("=" * 60)
print("CHROMADB PERSISTENT VECTOR STORE DEMO")
print("=" * 60)

initial_count = count()
print(f"Current collection document count: {initial_count}")

# Index two sample notes
note_1 = (
    "Photosynthesis is the process used by plants and other organisms to convert light energy "
    "into chemical energy that can later be released to fuel the organisms' activities."
)
meta_1 = {"filename": "bio_ch1.md", "subject": "biology"}

doc_id_1 = index_document(note_1, meta_1)
print(f"\nIndexed note 1 -> ID: {doc_id_1[:8]}... (Subject: {meta_1['subject']})")

note_2 = (
    "In classical mechanics, Newton's laws of motion are three basic laws describing the relation "
    "between the motion of an object and the forces acting on it."
)
meta_2 = {"filename": "phys_ch2.md", "subject": "physics"}

doc_id_2 = index_document(note_2, meta_2)
print(f"Indexed note 2 -> ID: {doc_id_2[:8]}... (Subject: {meta_2['subject']})")

print(f"\nNew collection document count: {count()} (+{count() - initial_count})")

# Query the database
query = "How do plants make energy?"
print(f"\nQuerying: '{query}'")
results = search(query, k=2)

for i, r in enumerate(results, 1):
    sim = round(1.0 - r["distance"], 4)
    print(f"\n[{i}] Distance: {r['distance']} (Similarity: {sim})")
    print(f"    Subject:  {r['metadata'].get('subject')}")
    print(f"    Snippet:  {r['text'][:80]}...")
