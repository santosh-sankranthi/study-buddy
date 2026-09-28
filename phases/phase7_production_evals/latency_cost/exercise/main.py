"""EXERCISE -- Stage Profiling & Bottleneck Identification.

The demo simulated timing across pipeline stages.
Your twist: implement analyze_pipeline_metrics() to calculate total latency,
identify the bottleneck stage (highest ms), and compute total USD cost.

Fill in every TODO. Run when done:
    python phases/phase7_production_evals/latency_cost/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens


# ── TODO(1): Implement analyze_pipeline_metrics ──────────────────────────────
def analyze_pipeline_metrics(
    stage_latencies_ms: dict[str, float],
    input_text: str,
    output_text: str,
    price_in: float = 0.50,
    price_out: float = 1.50,
) -> dict:
    """Analyze stage timings and token costs.

    Returns:
        {
            "total_latency_ms": float,
            "bottleneck_stage": str,
            "input_tokens": int,
            "output_tokens": int,
            "cost_usd": float,
        }
    """
    # TODO(1a): total_latency_ms = sum of all values in stage_latencies_ms
    tot_lat = round(sum(stage_latencies_ms.values()), 2)
    # TODO(1b): bottleneck_stage = key with max value in stage_latencies_ms
    bottleneck = max(stage_latencies_ms, key=stage_latencies_ms.get)
    # TODO(1c): compute input_tokens, output_tokens, and cost_usd
    in_tok = count_tokens(input_text)
    out_tok = count_tokens(output_text)
    cost = round((in_tok / 1_000_000 * price_in) + (out_tok / 1_000_000 * price_out), 6)

    return {
        "total_latency_ms": tot_lat,
        "bottleneck_stage": bottleneck,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "cost_usd": cost,
    }


# ── TODO(2): Record observation ──────────────────────────────────────────────
OBSERVATION = (
    "In full-pipeline RAG requests, generation decoding is almost always the latency bottleneck, "
    "making streaming and token length caps critical for user experience."
)


if __name__ == "__main__":
    latencies = {
        "embedding": 45.2,
        "retrieval": 12.1,
        "llm_generation": 420.5,
        "serialization": 2.3,
    }
    metrics = analyze_pipeline_metrics(
        latencies,
        "What is photosynthesis? " * 10,
        "Photosynthesis converts light into chemical energy.",
    )
    print("Metrics:", metrics)
    print("\nObservation:", OBSERVATION)
