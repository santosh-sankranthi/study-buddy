"""EXERCISE -- Fixed vs. Paragraph-Based Chunking.

The demo used chunk_fixed() with sliding word windows.
Your twist: compare chunk_fixed() with chunk_paragraph() on a structured 3-paragraph
study note, evaluating chunk counts, boundary cleanliness, and semantic coherence.

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/chunking/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed, chunk_paragraph

STUDY_NOTE = """# Chapter 1: Introduction to Ecology
Ecology is the study of how organisms interact with one another and with their physical environment. The distribution and abundance of organisms on Earth are shaped by both biotic and abiotic factors.

Biotic factors include interactions with other organisms, such as predation, parasitism, herbivory, competition, and symbiosis. These dynamic biological relationships maintain ecosystem stability.

Abiotic factors are nonliving physical and chemical components of an environment, including temperature, precipitation, sunlight, soil composition, and dissolved oxygen levels in aquatic biomes."""


# ── TODO(1): Run chunk_paragraph on STUDY_NOTE ───────────────────────────────
def get_paragraph_chunks(note: str = STUDY_NOTE) -> list[str]:
    """Return paragraph chunks using chunk_paragraph(note)."""
    # TODO(1): return chunk_paragraph(note)
    return chunk_paragraph(note)


# ── TODO(2): Run chunk_fixed on STUDY_NOTE ───────────────────────────────────
def get_fixed_chunks(note: str = STUDY_NOTE, size: int = 30, overlap: int = 10) -> list[str]:
    """Return fixed chunks using chunk_fixed(note, chunk_size=size, overlap=overlap)."""
    # TODO(2): return chunk_fixed(note, chunk_size=size, overlap=overlap)
    return chunk_fixed(note, chunk_size=size, overlap=overlap)


# ── TODO(3): Record your observation ─────────────────────────────────────────
OBSERVATION = (
    "Paragraph chunking cleanly isolates distinct topics (Overview, Biotic, Abiotic) "
    "without cutting sentences, while fixed chunking guarantees strict token upper bounds."
)


if __name__ == "__main__":
    p_chunks = get_paragraph_chunks()
    print(f"Paragraph chunking produced {len(p_chunks)} chunks:")
    for i, c in enumerate(p_chunks, 1):
        print(f"  [{i}] ({len(c.split())} words) {c[:50]}...")

    f_chunks = get_fixed_chunks()
    print(f"\nFixed chunking produced {len(f_chunks)} chunks:")
    for i, c in enumerate(f_chunks, 1):
        print(f"  [{i}] ({len(c.split())} words) {c[:50]}...")
    print("\nObservation:", OBSERVATION)
