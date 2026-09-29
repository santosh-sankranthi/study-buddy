"""EXERCISE -- Trace Summary.

Practice: add up duration, tokens and cost from a list of trace spans.
Task: finish summarize_trace() so it returns the three totals.

Check your work with:
    python phases/phase6_eval_observability/tracing/solution/check.py
"""

SAMPLE_SPANS = [
    {"name": "embed_query", "duration_ms": 120, "tokens": 15, "cost_usd": 0.000007},
    {"name": "vector_search", "duration_ms": 45, "tokens": 0, "cost_usd": 0.0},
    {"name": "llm_generate", "duration_ms": 1450, "tokens": 620, "cost_usd": 0.000310},
]


def summarize_trace(spans: list[dict]) -> dict:
    """Return the total duration_ms, tokens and cost_usd across `spans`."""
    # TODO: sum each field across the spans.
    raise NotImplementedError("summarize_trace")


if __name__ == "__main__":
    print(summarize_trace(SAMPLE_SPANS))
