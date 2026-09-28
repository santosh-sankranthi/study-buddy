"""EXERCISE -- Paragraph Chunking.

The demo implemented fixed-size chunking.
Your twist: implement chunk_paragraph() and get_paragraph_chunks() splitting on double-newlines.

Run when done:
    python phases/phase5_rag_pipeline/chunking/solution/check.py
"""
SAMPLE_NOTE = """Cell division is crucial for growth.
Mitosis produces two genetically identical diploid cells.

Meiosis, in contrast, produces four haploid gametes.
Crossing over during prophase I increases genetic diversity."""

# TODO(1): Implement chunk_paragraph(text: str) -> list[str]
def chunk_paragraph(text: str) -> list[str]:
    raise NotImplementedError("TODO(1): implement chunk_paragraph")

def get_paragraph_chunks() -> list[str]:
    raise NotImplementedError("TODO(2): implement get_paragraph_chunks")

if __name__ == "__main__":
    print(get_paragraph_chunks())
