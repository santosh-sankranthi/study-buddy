"""EXERCISE -- Threshold Tuning & Precision/Recall Trade-offs.

The demo showed threshold filtering on on-topic vs off-topic queries.
Your twist: measure the number of retrieved chunks for a query across
three thresholds: loose (0.10), balanced (0.35), and strict (0.95).

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/retrieval/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import retrieve

QUERY = "glucose breakdown and cellular ATP"

# TODO(1): Implement evaluate_thresholds(query: str, thresholds: list[float]) -> dict[float, int]
# For each threshold t, call retrieve(query, k=5, min_similarity=t)
# Return {t: len(results or [])}
def evaluate_thresholds(query: str = QUERY, thresholds: list[float] | None = None) -> dict[float, int]:
    raise NotImplementedError("TODO(1): implement evaluate_thresholds")


# TODO(2): Write ONE sentence explaining the trade-off of high vs low thresholds:
OBSERVATION = ""


if __name__ == "__main__":
    counts = evaluate_thresholds()
    print("Counts per threshold:", counts)
    print("Observation:", OBSERVATION)
