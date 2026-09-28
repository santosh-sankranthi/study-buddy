"""DEMO -- End-to-End Note Indexing Pipeline.

Live-code target: load raw text, chunk it using chunk_fixed, enrich each chunk
with metadata, and persist to ChromaDB via app.vector_store.index_document.

Run:
    python phases/phase5_rag_pipeline/indexing/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed
from app.vector_store import count, index_document

DOC_FILENAME = "cellular_respiration.md"
DOC_SUBJECT = "biology"
RAW_NOTE = (
    "# Cellular Respiration Summary\n\n"
    "Cellular respiration is a series of chemical reactions that break down glucose to produce ATP. "
    "Glycolysis occurs in the cytoplasm and breaks glucose into two pyruvate molecules, yielding a net of 2 ATP and 2 NADH. "
    "Pyruvate then enters the mitochondrial matrix for the citric acid cycle (Krebs cycle). "
    "The Krebs cycle produces CO2, ATP, NADH, and FADH2. "
    "Finally, oxidative phosphorylation via the electron transport chain across the inner mitochondrial membrane "
    "generates approximately 28 to 32 ATP molecules using oxygen as the terminal electron acceptor."
)

print("=" * 60)
print(f"INDEXING PIPELINE DEMO: {DOC_FILENAME}")
print("=" * 60)

before_count = count()
chunks = chunk_fixed(RAW_NOTE, chunk_size=30, overlap=10)
print(f"Generated {len(chunks)} chunks from source text.")

indexed_ids = []
for idx, chunk_text in enumerate(chunks):
    metadata = {
        "filename": DOC_FILENAME,
        "subject": DOC_SUBJECT,
        "chunk_index": idx,
        "total_chunks": len(chunks),
    }
    doc_id = index_document(chunk_text, metadata)
    indexed_ids.append(doc_id)
    print(f"  Indexed chunk {idx} -> ID: {doc_id[:8]}... ({len(chunk_text.split())} words)")

after_count = count()
print(f"\nCollection count: {before_count} -> {after_count} (+{after_count - before_count})")
