"""EXERCISE -- Long Context.

Practice: estimate the API cost of a prompt from its token count.

Task: finish calculate_cost() using (tokens / 1_000_000) * price_per_million.

Check your work with:
    python phases/phase2_context_engineering/long_context/solution/check.py
"""

TOKENS = 100_000


def calculate_cost(tokens: int, price_per_million: float = 0.50) -> float:
    """Return the dollar cost of `tokens` at the given price per million."""
    # TODO: convert tokens to millions and multiply by the price.
    raise NotImplementedError("calculate_cost")


if __name__ == "__main__":
    print("Cost for 100k tokens:", calculate_cost(TOKENS))
