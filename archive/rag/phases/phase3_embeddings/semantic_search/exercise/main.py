"""EXERCISE -- Custom Semantic Search Corpus.

The demo searched academic biology notes.
Your twist: provide at least 3 custom domain sentences in CUSTOM_CORPUS
and implement rank_custom_corpus(query: str) -> list[tuple[str, float]].

Run when done:
    python phases/phase3_embeddings/semantic_search/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Provide at least 3 distinct domain sentences
CUSTOM_CORPUS: list[str] = []

# TODO(2): Implement rank_custom_corpus(query: str) -> list[tuple[str, float]]
def rank_custom_corpus(query: str) -> list[tuple[str, float]]:
    raise NotImplementedError("TODO(2): implement rank_custom_corpus")

if __name__ == "__main__":
    print(rank_custom_corpus("energy"))
