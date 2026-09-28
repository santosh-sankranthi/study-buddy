"""EXERCISE -- Reusable Note Ingestion Function.

The demo indexed a single note inline.
Your twist: implement index_note_file() as a reusable ingestion function that
accepts raw text and metadata, splits it with chunk_fixed(), indexes each chunk
with {filename, subject, chunk_index, total_chunks}, and returns the list of doc IDs.

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/indexing/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed
from app.vector_store import count, index_document


# ── TODO(1): Implement index_note_file ───────────────────────────────────────
def index_note_file(
    text: str,
    filename: str,
    subject: str,
    chunk_size: int = 25,
    overlap: int = 5,
) -> list[str]:
    """Ingest, chunk, enrich, and index a document into ChromaDB.

    Returns the list of generated document IDs.
    """
    # TODO(1a): chunks = chunk_fixed(text, chunk_size=chunk_size, overlap=overlap)
    chunks = chunk_fixed(text, chunk_size=chunk_size, overlap=overlap)
    doc_ids = []
    # TODO(1b): for idx, c in enumerate(chunks):
    #             meta = {"filename": filename, "subject": subject, "chunk_index": idx, "total_chunks": len(chunks)}
    #             doc_id = index_document(c, meta)
    #             doc_ids.append(doc_id)
    for idx, c in enumerate(chunks):
        meta = {
            "filename": filename,
            "subject": subject,
            "chunk_index": idx,
            "total_chunks": len(chunks),
        }
        doc_ids.append(index_document(c, meta))
    return doc_ids


SAMPLE_NOTE = (
    "Electromagnetism is one of the four fundamental interactions in nature. "
    "It is described by Maxwell's equations, which unify electricity, magnetism, and optics. "
    "A changing magnetic field induces an electromotive force (Faraday's law of induction). "
    "Electromagnetic radiation travels through a vacuum at the speed of light."
)

if __name__ == "__main__":
    before = count()
    ids = index_note_file(SAMPLE_NOTE, "electromagnetism.md", "physics")
    print(f"Indexed {len(ids)} chunks from electromagnetism.md")
    print(f"Total collection count: {before} -> {count()}")
