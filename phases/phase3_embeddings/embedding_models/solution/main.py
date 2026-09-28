"""SOLUTION -- Batch Embedding Generation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import embed_batch

def get_sentence_embeddings() -> list[list[float]]:
    sentences = ["Plants absorb sunlight.", "Newton's second law is F=ma."]
    return embed_batch(sentences)

if __name__ == "__main__":
    print(len(get_sentence_embeddings()))
