"""EXERCISE -- Comprehensive Groundedness Test Suite.

The demo ran groundedness checks on isolated examples.
Your twist: implement evaluate_rag_test_suite() to run deterministic and LLM
groundedness checks over a test matrix of answers, returning pass/fail metrics.

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/eval_groundedness/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.evals.groundedness import check_groundedness, check_length_and_citation

TEST_CASES = [
    {
        "id": "grounded_valid",
        "context": "DNA is composed of two polynucleotide chains that coil around each other to form a double helix.",
        "answer": "DNA forms a double helix structure composed of two polynucleotide chains [Chunk 1 — genetics.md].",
        "expected_det": True,
        "expected_grounded": True,
    },
    {
        "id": "missing_citation",
        "context": "Enzymes act as biological catalysts by lowering activation energy.",
        "answer": "Enzymes speed up reactions by lowering activation energy.",
        "expected_det": False,  # Missing [Chunk ...] citation
        "expected_grounded": True,
    },
    {
        "id": "hallucination",
        "context": "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
        "answer": "Water boils at 100 degrees Celsius and turns into hydrogen gas bubbles [Chunk 1 — chem.md].",
        "expected_det": True,
        "expected_grounded": False,  # hydrogen gas bubbles is not in context!
    },
]


# ── TODO(1): Implement evaluate_rag_test_suite ───────────────────────────────
def evaluate_rag_test_suite(cases: list[dict] | None = None) -> list[dict]:
    """Run deterministic and groundedness checks on each test case.

    Returns list of dicts with {id, det_passed, grounded_passed}.
    """
    if cases is None:
        cases = TEST_CASES

    results = []
    # TODO(1): for c in cases:
    #             det = check_length_and_citation(c["answer"], max_words=50)
    #             grounded = check_groundedness(c["answer"], c["context"])
    #             results.append({"id": c["id"], "det_passed": det["passed"], "grounded_passed": grounded})
    for c in cases:
        det = check_length_and_citation(c["answer"], max_words=50)
        grounded = check_groundedness(c["answer"], c["context"])
        results.append({
            "id": c["id"],
            "det_passed": det["passed"],
            "grounded_passed": grounded,
        })
    return results


if __name__ == "__main__":
    res = evaluate_rag_test_suite()
    print("Test Suite Evaluation Results:")
    for r in res:
        print(f"  [{r['id']}] Deterministic: {r['det_passed']} | Grounded: {r['grounded_passed']}")
