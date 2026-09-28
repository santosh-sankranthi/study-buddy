"""EXERCISE -- Sampling: investigate top_p instead of temperature.

The demo ran the same prompt at temperature 0 vs 1.2 and showed how output
varies. Your twist: keep temperature fixed at 1.0 and vary top_p (0.1, 0.5, 1.0)
instead -- three runs each. Then write one sentence of observation.

Fill in every TODO. Run when done:
    python phases/phase0_fundamentals/sampling/solution/check.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PROMPT = "Give me ONE creative word that means 'to study intensely'. Just the word, nothing else."
N_RUNS = 3
FIXED_TEMPERATURE = 1.0

# TODO(1): For each p in [0.1, 0.5, 1.0], call chat() N_RUNS times:
#   chat([{"role": "user", "content": PROMPT}], temperature=FIXED_TEMPERATURE, top_p=p)
# Store results in a dictionary mapping top_p -> list of string replies.
results: dict[float, list[str]] = {}


# TODO(2): Write one sentence describing what you observed.
# How does changing top_p affect the diversity of results compared to temperature?
OBSERVATION = ""


if __name__ == "__main__":
    print(f"Prompt: {PROMPT!r}
")
    print(f"Fixed temperature: {FIXED_TEMPERATURE}
")

    for top_p, runs in results.items():
        print(f"--- top_p = {top_p} ---")
        for i, r in enumerate(runs, 1):
            print(f"  run {i}: {r!r}")
        print(f"  unique out of {N_RUNS}: {len(set(runs))}")
        print()

    print("Your observation:", OBSERVATION)
