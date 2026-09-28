"""EXERCISE -- Context Budget & Cost Modeling.

The demo printed scaling metrics for long context.
Your twist: implement calculate_cost() to compute the exact USD cost for a given
input/output token profile, model a multi-turn conversation cost curve, and record
an observation on why RAG is economically superior to long-context stuffing.

Fill in every TODO. Run when done:
    python phases/phase2_context_engineering/long_context/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))


# ── TODO(1): Implement calculate_cost ────────────────────────────────────────
def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    price_per_m_input: float = 0.50,
    price_per_m_output: float = 1.50,
) -> float:
    """Calculate the total cost in USD for the given token quantities.

    Returns the total cost rounded to 6 decimal places.
    """
    # TODO(1): input_cost = (input_tokens / 1_000_000) * price_per_m_input
    #          output_cost = (output_tokens / 1_000_000) * price_per_m_output
    #          return round(input_cost + output_cost, 6)
    input_cost = (input_tokens / 1_000_000) * price_per_m_input
    output_cost = (output_tokens / 1_000_000) * price_per_m_output
    return round(input_cost + output_cost, 6)


# ── TODO(2): Model a 10-turn conversation cost ───────────────────────────────
def model_10_turn_session(doc_tokens: int, turns: int = 10) -> float:
    """If the entire document (doc_tokens) is re-sent on every turn alongside 100 question tokens,

    plus 300 response tokens per turn, calculate total session cost.
    """
    total = 0.0
    for _ in range(turns):
        turn_input = doc_tokens + 100
        turn_output = 300
        total += calculate_cost(turn_input, turn_output)
    return round(total, 6)


# ── TODO(3): Record your observation on stuffing vs. RAG ─────────────────────
OBSERVATION = (
    "Stuffing the full document repeatedly causes costs to scale linearly with turn count, "
    "whereas RAG retrieves only relevant chunks, keeping per-turn input tokens constant and low."
)


if __name__ == "__main__":
    for doc_size in [1_000, 10_000, 100_000]:
        cost = model_10_turn_session(doc_size)
        print(f"10-turn session with {doc_size:>7} doc tokens: ${cost:.4f}")
    print("\nObservation:", OBSERVATION)
