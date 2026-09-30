"""SOLUTION -- Regression Pass Rate.

Reference answer: score each answer by substring match, then compute the rate.
"""

EVAL_CASES = [
    {"question": "Which pigment absorbs light?", "expected_substr": "chlorophyll", "answer": "Chlorophyll absorbs light."},
    {"question": "Where does photosynthesis occur?", "expected_substr": "chloroplast", "answer": "Inside the chloroplast."},
    {"question": "Which gas is released?", "expected_substr": "oxygen", "answer": "Oxygen is released."},
    {"question": "Which organelle makes ATP?", "expected_substr": "mitochondria", "answer": "The mitochondria make ATP."},
    {"question": "State Newton's second law.", "expected_substr": "force", "answer": "Force equals mass times acceleration."},
]


def run_regression_suite(cases: list[dict]) -> dict:
    """Return {"total", "passed", "pass_rate"} for the given cases."""
    hits = [c["expected_substr"].lower() in c["answer"].lower() for c in cases]
    total = len(cases)
    return {
        "total": total,
        "passed": sum(hits),
        "pass_rate": sum(hits) / total if total else 0.0,
    }


if __name__ == "__main__":
    print(run_regression_suite(EVAL_CASES))
