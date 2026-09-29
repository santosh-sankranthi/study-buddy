"""Practice: see how top_p changes the variety of sampled answers.
Task: finish sample() so it calls the model N_RUNS times at the given top_p.
Check your work with: python phases/phase0_fundamentals/sampling/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PROMPT = "Give me ONE creative word that means 'to study intensely'. Just the word, nothing else."
TEMPERATURE = 1.0
TOP_P_VALUES = [0.1, 0.5, 1.0]
N_RUNS = 3


def build_messages() -> list[dict]:
    """The single user message we send to the model."""
    return [{"role": "user", "content": PROMPT}]


def sample(top_p: float, n_runs: int) -> list[str]:
    """Return n_runs stripped replies at the fixed temperature and this top_p."""
    # TODO: call chat(build_messages(), temperature=TEMPERATURE, top_p=top_p)
    # n_runs times and collect the stripped replies.
    raise NotImplementedError("sample")


if __name__ == "__main__":
    for top_p in TOP_P_VALUES:
        replies = sample(top_p, N_RUNS)
        print(f"top_p={top_p}: {len(set(replies))}/{N_RUNS} unique -> {replies}")
