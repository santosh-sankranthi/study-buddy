"""SOLUTION -- Trace Summary.

Reference answer: sum each field across the spans.
"""

SAMPLE_SPANS = [
    {"name": "embed_query", "duration_ms": 120, "tokens": 15, "cost_usd": 0.000007},
    {"name": "vector_search", "duration_ms": 45, "tokens": 0, "cost_usd": 0.0},
    {"name": "llm_generate", "duration_ms": 1450, "tokens": 620, "cost_usd": 0.000310},
]


def summarize_trace(spans: list[dict]) -> dict:
    """Return the total duration_ms, tokens and cost_usd across `spans`."""
    return {
        "total_duration_ms": sum(s["duration_ms"] for s in spans),
        "total_tokens": sum(s["tokens"] for s in spans),
        "total_cost_usd": round(sum(s["cost_usd"] for s in spans), 6),
    }


if __name__ == "__main__":
    print(summarize_trace(SAMPLE_SPANS))
