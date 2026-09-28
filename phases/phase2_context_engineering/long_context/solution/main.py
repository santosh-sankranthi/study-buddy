"""SOLUTION -- Long Context Cost Measurement."""
def calculate_cost(tokens: int, price_per_million: float = 0.50) -> float:
    return round((tokens / 1_000_000.0) * price_per_million, 6)

OBSERVATION = "Passing entire documents directly into context causes linear cost escalation and quadratic attention latency, motivating targeted RAG retrieval."

if __name__ == "__main__":
    print(calculate_cost(100_000))
