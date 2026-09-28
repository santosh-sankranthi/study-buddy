"""EXERCISE -- Tokens (your twist).

The demo counted a fixed sentence under one encoding. Your twist:

  1. use YOUR OWN paragraph, and
  2. count it under TWO different encodings, then
  3. explain, in one sentence, why the two counts differ (or why they don't).

Fill in every `TODO(n)`. When you are done run:

    python phases/phase0_fundamentals/tokens/solution/check.py
"""

import tiktoken

# TODO(0): Replace this with YOUR OWN paragraph -- at least 3 sentences / 20
# words. Pick something with a few unusual or long words so the two encodings
# have something to disagree about. Do NOT reuse the demo sentence.
PARAGRAPH = "TODO: paste your own paragraph here."

# TODO(3): Once you have printed both counts, write ONE plain-English sentence
# here explaining the difference. No code.
EXPLANATION = ""


def count_tokens(text: str, encoding_name: str) -> int:
    """Return the number of tokens in `text` under the named encoding.

    TODO(1): create the encoding with `tiktoken.get_encoding(encoding_name)`,
    encode the text, and return how many IDs came back.
    """
    raise NotImplementedError("TODO(1): count the tokens")


def main() -> dict:
    """Print the token count of PARAGRAPH under both encodings and return them.

    TODO(2):
      - call count_tokens() for "cl100k_base" AND for "o200k_base"
      - PRINT each count (so it shows up when the script runs)
      - return a dict of the form {"cl100k_base": <int>, "o200k_base": <int>}
    """
    raise NotImplementedError("TODO(2): count under both encodings")


if __name__ == "__main__":
    counts = main()
    print("counts     :", counts)
    print("explanation:", EXPLANATION)
