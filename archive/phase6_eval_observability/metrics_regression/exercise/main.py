"""EXERCISE -- Regression Pass Rate.

Practice: score golden answers and compute a pass rate.
Task: finish run_regression_suite() so a case passes when its expected_substr
appears in its answer.

Check your work with:
    python phases/phase6_eval_observability/metrics_regression/solution/check.py
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
    # TODO: count cases whose expected_substr appears in their answer.
    raise NotImplementedError("run_regression_suite")


if __name__ == "__main__":
    print(run_regression_suite(EVAL_CASES))
