"""EXERCISE -- Threshold Tuning & Precision/Recall Trade-offs.

The demo showed threshold filtering on on-topic vs off-topic queries.
Your twist: measure the number of retrieved chunks for an on-topic query across
three thresholds: loose (0.10), balanced (0.35), and strict (0.95), verifying that
higher thresholds increase precision but risk zero recall.

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/retrieval/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import retrieve

QUERY = "glucose breakdown and cellular ATP"


# ── TODO(1): Evaluate retrieve across thresholds ─────────────────────────────
def evaluate_thresholds(
    query: str = QUERY,
    thresholds: list[float] | None = None,
) -> dict[float, int]:
    """Test query across thresholds and return dict of {threshold: count_of_chunks}."""
    if thresholds is None:
        thresholds = [0.10, 0.35, 0.95]

    results = {}
    # TODO(1): for t in thresholds:
    #             res = retrieve(query, k=5, min_similarity=t)
    #             results[t] = len(res) if res is not None else 0
    for t in thresholds:
        res = retrieve(query, k=5, min_similarity=t)
        results[t] = len(res) if res is not None else 0
    return results


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "Lower thresholds maximize recall but risk admitting noisy chunks; "
    "strict thresholds ensure high precision but may reject valid partial matches."
)


if __name__ == "__main__":
    counts = evaluate_thresholds()
    print("Threshold evaluation results for query:", QUERY)
    for t, cnt in counts.items():
        print(f"  Threshold {t:0.2f}: {cnt} chunks passed")
    print("\nObservation:", OBSERVATION)
