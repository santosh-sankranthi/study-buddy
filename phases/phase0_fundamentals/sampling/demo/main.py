"""DEMO -- Sampling & Temperature.

Live-code target: run the SAME prompt at temperature 0 vs 1.2, three times each,
and show the class how the output varies (or doesn't).

Run:  python phases/phase0_fundamentals/sampling/demo/main.py

Key insight: temperature scales the probability distribution over the vocabulary.
Low → sharp peak → consistent. High → flat → creative but unpredictable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat  # noqa: E402

# A deliberately open-ended prompt so variation is obvious.
PROMPT = "Give me ONE creative word that means 'to study intensely'. Just the word, nothing else."

N_RUNS = 3


def run_at_temperature(temperature: float) -> list[str]:
    results = []
    for i in range(N_RUNS):
        answer = chat(
            [{"role": "user", "content": PROMPT}],
            temperature=temperature,
        )
        results.append(answer.strip())
    return results


if __name__ == "__main__":
    print(f"Prompt: {PROMPT!r}\n")

    for temp in [0.0, 1.2]:
        print(f"--- temperature = {temp} ---")
        results = run_at_temperature(temp)
        for i, r in enumerate(results, 1):
            print(f"  run {i}: {r!r}")
        unique = len(set(results))
        print(f"  unique answers out of {N_RUNS}: {unique}")
        print()

    print("Key: temperature=0 → same answer every time (argmax).")
    print("     temperature=1.2 → much more variety; often different each run.")
    print()
    print("Next concept: how does this change when we vary top_p instead?")
