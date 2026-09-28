"""SOLUTION -- Paragraph Chunking."""
import re

SAMPLE_NOTE = """Cell division is crucial for growth.
Mitosis produces two genetically identical diploid cells.

Meiosis, in contrast, produces four haploid gametes.
Crossing over during prophase I increases genetic diversity."""

def chunk_paragraph(text: str) -> list[str]:
    raw_paras = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in raw_paras if p.strip()]

def get_paragraph_chunks() -> list[str]:
    return chunk_paragraph(SAMPLE_NOTE)

if __name__ == "__main__":
    print(get_paragraph_chunks())
