"""SOLUTION -- Metadata-Filtered Similarity Search."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import index_document, search

def seed_chemistry_notes() -> list[str]:
    docs = [
        ("Solubility rules dictate which ionic compounds precipitate.", {"subject": "chemistry"}),
        ("Acids donate protons while bases accept protons.", {"subject": "chemistry"}),
    ]
    return [index_document(text, meta) for text, meta in docs]

def search_chemistry(query: str) -> list[dict]:
    return search(query, k=2, subject="chemistry")

if __name__ == "__main__":
    seed_chemistry_notes()
    print(search_chemistry("precipitation"))
