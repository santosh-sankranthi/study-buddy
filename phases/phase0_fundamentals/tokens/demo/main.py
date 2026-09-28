"""DEMO -- Tokens.

Live-code target: show that an LLM sees tokens, not words.

Run:  python phases/phase0_fundamentals/tokens/demo/main.py

Nothing here touches the network. It is pure measurement: that is the point.
"""

import tiktoken  # the reference tokenizer

# Pick one fixed sentence so the class sees the same numbers.
SENTENCE = "Study Buddy turns your notes into answers, not guesses."

# 1. Load a tokenizer. "cl100k_base" is the GPT-4/3.5 family encoding.
encoding = tiktoken.get_encoding("cl100k_base")

# 2. Turn the text into token IDs (integers).
token_ids = encoding.encode(SENTENCE)

# 3. Show the actual pieces so the class can see words being split.
print("text  :", SENTENCE)
print("chars :", len(SENTENCE), " words:", len(SENTENCE.split()))
print("tokens:", len(token_ids))
print()
for position, token_id in enumerate(token_ids):
    piece = encoding.decode([token_id])
    print(f"  {position:>2}  id={token_id:<6} {piece!r}")

print()
print(f"ratio : {len(SENTENCE) / len(token_ids):.2f} chars per token")
print("Note: 'tokens' is almost never equal to 'words'. Everything in the API")
print("-- cost, latency, context limits -- is measured in these units.")
