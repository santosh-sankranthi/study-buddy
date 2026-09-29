"""SOLUTION -- Tokens.

Reference answer: encode the text and return the number of tokens.
"""

import tiktoken

TEXT = "Polymorphism lets different classes answer the same method call."


def count_tokens(text: str, encoding: str) -> int:
    """Return how many tokens `text` becomes under `encoding`."""
    return len(tiktoken.get_encoding(encoding).encode(text))


if __name__ == "__main__":
    print("cl100k:", count_tokens(TEXT, "cl100k_base"))
    print("o200k :", count_tokens(TEXT, "o200k_base"))
