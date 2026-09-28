"""EXERCISE -- Regression Test Suite & Pass-Rate Delta.

The demo evaluated pass rates across prompt variations.
Your twist: define EVAL_CASES with at least 5 questions and assertions,
and implement run_regression_suite(cases) -> dict.

Run when done:
    python phases/phase6_eval_observability/metrics_regression/solution/check.py
"""
# TODO(1): Provide at least 5 eval test cases: [{"question": str, "expected_substr": str}]
EVAL_CASES: list[dict] = []

# TODO(2): Implement run_regression_suite(cases) -> dict
# Return {"total": int, "passed": int, "pass_rate": float}
def run_regression_suite(cases: list[dict] | None = None) -> dict:
    raise NotImplementedError("TODO(2): implement run_regression_suite")

if __name__ == "__main__":
    print(run_regression_suite())
