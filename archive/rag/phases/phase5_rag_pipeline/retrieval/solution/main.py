"""SOLUTION -- Retrieval Threshold Evaluation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import retrieve

QUERY = "glucose breakdown and cellular ATP"

def evaluate_thresholds(query: str = QUERY, thresholds: list[float] | None = None) -> dict[float, int]:
    if thresholds is None:
        thresholds = [0.10, 0.35, 0.95]
    res = {}
    for t in thresholds:
        chunks = retrieve(query, k=5, min_similarity=t)
        res[t] = len(chunks) if chunks is not None else 0
    return res

OBSERVATION = "Higher similarity thresholds increase precision but risk complete recall failure if the question wording differs from the notes."

if __name__ == "__main__":
    print(evaluate_thresholds())
