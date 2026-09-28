"""EXERCISE -- Latency and Cost Breakdown from Trace.

The demo visualized execution latency timelines.
Your twist: implement summarize_trace(spans: list[dict]) -> dict
calculating total_duration_ms, total_tokens, and total_cost_usd.

Run when done:
    python phases/phase9_eval_observability/tracing/solution/check.py
"""
SAMPLE_SPANS = [
    {"name": "embed_query", "duration_ms": 120, "tokens": 15, "cost_usd": 0.000007},
    {"name": "vector_search", "duration_ms": 45, "tokens": 0, "cost_usd": 0.0},
    {"name": "llm_generate", "duration_ms": 1450, "tokens": 620, "cost_usd": 0.000310},
]

# TODO(1): Implement summarize_trace(spans: list[dict]) -> dict
# Return {"total_duration_ms": int, "total_tokens": int, "total_cost_usd": float}
def summarize_trace(spans: list[dict] | None = None) -> dict:
    raise NotImplementedError("TODO(1): implement summarize_trace")

if __name__ == "__main__":
    print(summarize_trace(SAMPLE_SPANS))
