"""EXERCISE -- Automated Triad Benchmark Scoring.

The demo evaluated a single query using RAG Triad heuristics.
Your twist: implement evaluate_triad_suite() to compute Context Relevance,
Faithfulness, and Answer Relevance across a multi-case benchmark dataset,
returning aggregate metrics and passing status against an 0.80 threshold.

Fill in every TODO. Run when done:
    python phases/phase9_advanced_capstone/eval_frameworks/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

TEST_RECORDS = [
    {
        "query": "What organelle performs photosynthesis?",
        "context": "Photosynthesis occurs within plant cell chloroplasts.",
        "answer": "Photosynthesis takes place in chloroplasts.",
        "expected_pass": True,
    },
    {
        "query": "What is Newton's second law formula?",
        "context": "Newton's second law is formulated as F = ma.",
        "answer": "Newton's second law states that Force = mass * acceleration (F=ma).",
        "expected_pass": True,
    },
    {
        "query": "How many chromosomes in humans?",
        "context": "Human cells have 46 chromosomes.",
        "answer": "Humans have 100 chromosomes.",  # Unfaithful hallucination
        "expected_pass": False,
    },
]


# ── TODO(1): Implement evaluate_triad_suite ──────────────────────────────────
def score_single_case(query: str, context: str, answer: str) -> float:
    """Return composite score between 0.0 and 1.0."""
    import re
    q_words = {w for w in re.findall(r"\w+", query.lower()) if len(w) > 3}
    c_words = set(re.findall(r"\w+", context.lower()))
    a_words = {w for w in re.findall(r"\w+", answer.lower()) if len(w) > 3}

    ctx_score = len(q_words & c_words) / max(len(q_words), 1)
    faith_score = len(a_words & c_words) / max(len(a_words), 1)

    # Penalize blatant numeric hallucinations
    num_ans = set(re.findall(r"\b\d+\b", answer))
    num_ctx = set(re.findall(r"\b\d+\b", context))
    if num_ans and not (num_ans & num_ctx):
        faith_score = 0.0

    return round((ctx_score + faith_score) / 2.0, 2)


def evaluate_triad_suite(
    records: list[dict] | None = None,
    threshold: float = 0.50,
) -> dict:
    """Evaluate records and return {scores: list[float], avg_score: float, passed: bool}."""
    if records is None:
        records = TEST_RECORDS

    scores = []
    # TODO(1): for r in records: compute score_single_case, append to scores
    for r in records:
        s = score_single_case(r["query"], r["context"], r["answer"])
        scores.append(s)

    avg = round(sum(scores) / len(scores), 2) if scores else 0.0

    return {
        "scores": scores,
        "avg_score": avg,
        "passed": avg >= threshold,
    }


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "The RAG Triad isolates the exact point of pipeline failure: low context relevance "
    "signals a retrieval problem, low faithfulness signals a prompt or hallucination problem, "
    "and low answer relevance signals query misalignment."
)


if __name__ == "__main__":
    res = evaluate_triad_suite()
    print("Triad Suite Results:", res)
    print("\nObservation:", OBSERVATION)
