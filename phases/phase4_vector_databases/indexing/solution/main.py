"""SOLUTION -- Ingest Document Batch."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import count, index_document

def index_cs_notes() -> list[str]:
    docs = [
        ("Recursion involves base cases and recursive steps.", {"subject": "cs", "topic": "recursion"}),
        ("Binary trees have at most two child nodes per parent.", {"subject": "cs", "topic": "trees"}),
    ]
    return [index_document(text, meta) for text, meta in docs]

if __name__ == "__main__":
    print(index_cs_notes())
