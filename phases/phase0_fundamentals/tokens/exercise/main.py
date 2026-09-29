"""EXERCISE -- Tokens.

Practice: turn text into tokens and watch the count change with the encoding.

Task: finish count_tokens() so it returns how many tokens `text` becomes.

Check your work with:
    python phases/phase0_fundamentals/tokens/solution/check.py
"""

import tiktoken

TEXT = "Polymorphism lets different classes answer the same method call."


def count_tokens(text: str, encoding: str) -> int:
    """Return how many tokens `text` becomes under `encoding`."""
    # TODO: get the encoding, encode the text, and return the number of tokens.
    raise NotImplementedError("count_tokens")


if __name__ == "__main__":
    print("cl100k:", count_tokens(TEXT, "cl100k_base"))
    print("o200k :", count_tokens(TEXT, "o200k_base"))
