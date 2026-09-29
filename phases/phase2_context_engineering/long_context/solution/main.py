"""SOLUTION -- Long Context.

Reference answer: convert tokens to millions and multiply by the price.
"""

TOKENS = 100_000


def calculate_cost(tokens: int, price_per_million: float = 0.50) -> float:
    """Return the dollar cost of `tokens` at the given price per million."""
    return (tokens / 1_000_000) * price_per_million


if __name__ == "__main__":
    print("Cost for 100k tokens:", calculate_cost(TOKENS))
