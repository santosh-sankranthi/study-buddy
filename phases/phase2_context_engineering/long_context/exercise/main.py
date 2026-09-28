"""EXERCISE -- Long Context Cost Measurement.

The demo measured latency across token counts.
Your twist: implement calculate_cost(tokens: int, price_per_million: float = 0.50) -> float
and record an observation on cost growth.

Run when done:
    python phases/phase2_context_engineering/long_context/solution/check.py
"""
# TODO(1): Implement calculate_cost(tokens: int, price_per_million: float = 0.50) -> float
# Formula: (tokens / 1_000_000) * price_per_million
def calculate_cost(tokens: int, price_per_million: float = 0.50) -> float:
    raise NotImplementedError("TODO(1): implement calculate_cost")

# TODO(2): Write one sentence describing the cost-latency tradeoff of stuffing full documents into context:
OBSERVATION = ""

if __name__ == "__main__":
    print("Cost for 100k tokens:", calculate_cost(100_000))
    print("Observation:", OBSERVATION)
