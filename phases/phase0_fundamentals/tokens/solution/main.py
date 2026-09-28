"""SOLUTION -- Tokens (reference answer to the twist).

Reference implementation of the exercise's three TODOs.
"""

import tiktoken

PARAGRAPH = (
    "Polymorphism lets objects of different classes respond to the same method "
    "call in their own way. In Python, duck typing means we rarely declare "
    "interfaces explicitly; instead we rely on whether an object implements the "
    "methods we invoke. This makes generic algorithms concise, but it pushes "
    "type errors from compile time to runtime."
)

EXPLANATION = (
    "o200k_base uses a larger vocabulary trained on more languages and code, so "
    "it usually splits the same text into equal or fewer tokens than cl100k_base."
)


def count_tokens(text: str, encoding_name: str) -> int:
    """Return the number of tokens in `text` under the named encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def main() -> dict:
    """Print and return the token count of PARAGRAPH under both encodings."""
    counts = {
        "cl100k_base": count_tokens(PARAGRAPH, "cl100k_base"),
        "o200k_base": count_tokens(PARAGRAPH, "o200k_base"),
    }
    for name, count in counts.items():
        print(f"{name:>12}: {count} tokens")
    return counts


if __name__ == "__main__":
    main()
