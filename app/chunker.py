"""Text chunking utilities.

Grows through the phases:
  Phase 5.1 — chunk_fixed() (token-aware fixed-size with overlap)
  Phase 5.1 (exercise) — chunk_paragraph()
"""

from __future__ import annotations

from common.tokens import count_tokens


# ── Phase 5.1: Fixed-size chunking ───────────────────────────────────────────

def chunk_fixed(text: str, chunk_size: int = 200, overlap: int = 50) -> list[str]:
    """Split *text* into overlapping fixed-size token windows.

    Works on words (a reasonable approximation when tiktoken isn't worth the
    overhead for every upload). Each chunk is at most *chunk_size* tokens wide;
    consecutive chunks share *overlap* words of context.

    Args:
        text:       The document text to split.
        chunk_size: Max tokens per chunk (approximate — measured in words here).
        overlap:    Number of words shared between consecutive chunks.

    Returns:
        A list of chunk strings, each non-empty.
    """
    if not text.strip():
        return []
    words  = text.split()
    chunks = []
    i      = 0
    while i < len(words):
        end   = i + chunk_size
        chunk = " ".join(words[i:end])
        if chunk.strip():
            chunks.append(chunk)
        if end >= len(words):
            break
        i += chunk_size - overlap   # slide forward by (size - overlap)
    return chunks


# ── Phase 5.1 exercise: Paragraph-based chunking ─────────────────────────────

def chunk_paragraph(text: str) -> list[str]:
    """Split *text* on double-newlines, keeping only non-empty paragraphs.

    Produces semantically coherent chunks when the document is well-structured.
    """
    return [p.strip() for p in text.split("\n\n") if p.strip()]
