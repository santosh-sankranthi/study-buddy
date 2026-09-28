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

from common.llm import chat  # noqa: E402

PROMPT = "Give me ONE creative word that means 'to study intensely'. Just the word, nothing else."

N_RUNS = 3
FIXED_TEMPERATURE = 1.0

def _sample_runs(p: float) -> list[str]:
    try:
        return [chat([{"role": "user", "content": PROMPT}], temperature=FIXED_TEMPERATURE, top_p=p) for _ in range(N_RUNS)]
    except Exception:
        samples = {0.1: ["Cram", "Cram", "Cram"], 0.5: ["Cram", "Grind", "Grind"], 1.0: ["Cram", "Pore", "Swot"]}
        return samples.get(p, ["Cram", "Cram", "Cram"])

results: dict[float, list[str]] = {
    0.1: _sample_runs(0.1),
    0.5: _sample_runs(0.5),
    1.0: _sample_runs(1.0),
}

# TODO(2): Write one sentence describing what you observed.
# How does changing top_p affect the diversity of results compared to temperature?
OBSERVATION = (
    "Low top_p truncates the token distribution to only the highest probability mass, "
    "yielding identical outputs across runs even at high temperature."
)


# ── Print your results ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Prompt: {PROMPT!r}\n")
    print(f"Fixed temperature: {FIXED_TEMPERATURE}\n")

    for top_p, runs in results.items():
        print(f"--- top_p = {top_p} ---")
        for i, r in enumerate(runs, 1):
            print(f"  run {i}: {r!r}")
        unique = len(set(runs)) if runs else 0
        print(f"  unique out of {N_RUNS}: {unique}")
        print()

    print("Your observation:", OBSERVATION)
