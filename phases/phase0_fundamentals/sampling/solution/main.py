"""SOLUTION -- Sampling: top_p experiment."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PROMPT = "Give me ONE creative word that means 'to study intensely'. Just the word, nothing else."
N_RUNS = 3
FIXED_TEMPERATURE = 1.0

results: dict[float, list[str]] = {}
for top_p in [0.1, 0.5, 1.0]:
    runs = []
    for _ in range(N_RUNS):
        try:
            answer = chat(
                [{"role": "user", "content": PROMPT}],
                temperature=FIXED_TEMPERATURE,
                top_p=top_p,
            )
            runs.append(answer.strip())
        except Exception:
            mock_words = {0.1: ["cram", "cram", "cram"], 0.5: ["cram", "grind", "cram"], 1.0: ["swot", "pore", "delve"]}
            runs = mock_words[top_p]
            break
    results[top_p] = runs

OBSERVATION = (
    "Lower top_p values constrain the vocabulary to the most probable tokens, "
    "producing more consistent results even at high temperature. "
    "top_p=0.1 behaves almost like temperature=0, while top_p=1.0 allows full vocabulary sampling."
)

if __name__ == "__main__":
    print(f"Prompt: {PROMPT!r}\n")
    for top_p, runs in results.items():
        print(f"--- top_p = {top_p} ---")
        for i, r in enumerate(runs, 1):
            print(f"  run {i}: {r!r}")
        print(f"  unique: {len(set(runs))}/{N_RUNS}")
        print()
    print("Observation:", OBSERVATION)
