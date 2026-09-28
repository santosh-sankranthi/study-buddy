"""DEMO -- Fixed-Size Chunking with Overlap.

Live-code target: examine chunk_fixed() in app.chunker, observe sliding window
progression across a text, and identify how overlapping words preserve boundary context.

Run:
    python phases/phase5_rag_pipeline/chunking/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed

SAMPLE_TEXT = (
    "Photosynthesis is a process used by plants to convert light into chemical energy. "
    "The process takes place inside plant organelles called chloroplasts. "
    "Within chloroplasts, chlorophyll absorbs light primarily in the blue and red wavelengths. "
    "Water is absorbed by roots and transported through the xylem to the leaves. "
    "Carbon dioxide enters the leaves through microscopic pores called stomata. "
    "The light reactions produce ATP and NADPH while releasing oxygen gas. "
    "The Calvin cycle uses ATP and NADPH to fix carbon dioxide into three-carbon sugars."
)

print("=" * 60)
print("FIXED CHUNKING DEMO (size=20 words, overlap=5 words)")
print("=" * 60)

chunks = chunk_fixed(SAMPLE_TEXT, chunk_size=20, overlap=5)
print(f"Total input words:  {len(SAMPLE_TEXT.split())}")
print(f"Total chunks created: {len(chunks)}\n")

for i, ch in enumerate(chunks, 1):
    words = ch.split()
    print(f"Chunk {i} ({len(words)} words):")
    print(f"  \"{ch}\"")
    if i < len(chunks):
        next_words = chunks[i].split()
        overlap_found = set(words[-5:]) & set(next_words[:5])
        print(f"  [Shared boundary words: {list(overlap_found)}]\n")
