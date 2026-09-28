"""DEMO -- Grounded Prompt Construction & Citation Extraction.

Live-code target: build a constrained RAG prompt using app.rag.build_rag_prompt(),
inspect the generated system and user messages, and extract source filenames.

Run:
    python phases/phase5_rag_pipeline/grounded_generation/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.rag import build_rag_prompt, extract_sources

MOCK_CHUNKS = [
    {
        "text": "Glycolysis yields a net gain of 2 ATP and 2 NADH molecules per glucose.",
        "metadata": {"filename": "cellular_respiration.md", "chunk_index": 0},
    },
    {
        "text": "Oxidative phosphorylation produces the majority of ATP in cellular respiration.",
        "metadata": {"filename": "cellular_respiration.md", "chunk_index": 3},
    },
    {
        "text": "Photosynthesis produces ATP during the light reactions in the thylakoid membrane.",
        "metadata": {"filename": "photosynthesis_ch4.md", "chunk_index": 1},
    },
]

QUESTION = "How many ATP molecules does glycolysis produce?"

print("=" * 60)
print("GROUNDED RAG PROMPT DEMO")
print("=" * 60)

messages = build_rag_prompt(QUESTION, MOCK_CHUNKS)
sources = extract_sources(MOCK_CHUNKS)

print(f"\nExtracted Source Files: {sources}")
print("\n--- System Message ---")
print(messages[0]["content"])

print("\n--- User Message (First 250 chars) ---")
print(messages[1]["content"][:250], "...")
