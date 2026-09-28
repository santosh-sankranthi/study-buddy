"""SOLUTION -- Custom Semantic Search Corpus."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import cosine_similarity, embed

CUSTOM_CORPUS: list[str] = [
    "Photosynthesis produces glucose and oxygen from sunlight.",
    "Cellular respiration consumes glucose to produce ATP in mitochondria.",
    "The Calvin cycle fixes atmospheric carbon dioxide in the chloroplast stroma.",
]

def rank_custom_corpus(query: str) -> list[tuple[str, float]]:
    q_vec = embed(query)
    scored = [(doc, cosine_similarity(q_vec, embed(doc))) for doc in CUSTOM_CORPUS]
    return sorted(scored, key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    print(rank_custom_corpus("ATP energy"))
