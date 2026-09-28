"""EXERCISE -- Metadata-Filtered Similarity Search.

The demo queried without filters.
Your twist: implement seed_chemistry_notes() and search_chemistry().

Run when done:
    python phases/phase4_vector_databases/similarity_search/solution/check.py
"""
# TODO(1): Implement seed_chemistry_notes() -> list[str]
def seed_chemistry_notes() -> list[str]:
    raise NotImplementedError("TODO(1): implement seed_chemistry_notes")

# TODO(2): Implement search_chemistry(query: str) -> list[dict]
def search_chemistry(query: str) -> list[dict]:
    raise NotImplementedError("TODO(2): implement search_chemistry")

if __name__ == "__main__":
    seed_chemistry_notes()
    print(search_chemistry("precipitation"))
