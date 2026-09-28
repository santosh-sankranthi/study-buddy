"""SOLUTION -- Reusable Note Ingestion Function."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed
from app.vector_store import count, index_document

def index_note_file(
    text: str,
    filename: str,
    subject: str,
    chunk_size: int = 25,
    overlap: int = 5,
) -> list[str]:
    chunks = chunk_fixed(text, chunk_size=chunk_size, overlap=overlap)
    doc_ids = []
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
    "It is described by Maxwell's equations, which unify electricity, magnetism, and optics."
)

if __name__ == "__main__":
    print(index_note_file(SAMPLE_NOTE, "electromagnetism.md", "physics"))
