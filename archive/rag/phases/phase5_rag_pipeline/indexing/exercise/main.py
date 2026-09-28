"""EXERCISE -- Reusable Note Ingestion Function.

The demo indexed a single note inline.
Your twist: implement index_note_file() as a reusable ingestion function that
accepts raw text and metadata, splits it with chunk_fixed(), indexes each chunk
with {filename, subject, chunk_index, total_chunks}, and returns the list of doc IDs.

Run when done:
    python phases/phase5_rag_pipeline/indexing/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed
from app.vector_store import count, index_document

# TODO(1): Implement index_note_file(text, filename, subject, chunk_size=25, overlap=5) -> list[str]
def index_note_file(
    text: str,
    filename: str,
    subject: str,
    chunk_size: int = 25,
    overlap: int = 5,
) -> list[str]:
    raise NotImplementedError("TODO(1): implement index_note_file")

SAMPLE_NOTE = (
    "Electromagnetism is one of the four fundamental interactions in nature. "
    "It is described by Maxwell's equations, which unify electricity, magnetism, and optics."
)

if __name__ == "__main__":
    print(index_note_file(SAMPLE_NOTE, "electromagnetism.md", "physics"))
