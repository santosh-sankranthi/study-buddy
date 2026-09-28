"""DEMO -- Context Windows.

Live-code target: watch a request grow until it hits the window, and see what
"over budget" looks like.

Run:  python phases/phase0_fundamentals/context_window/demo/main.py

This demo is deterministic and offline by default: instead of waiting for a real
API error, it simulates a small context window so the failure is instant and
repeatable in class. Pass --live to send a real request that is over budget and
see the provider's error instead.
"""

import argparse
import os
import sys
from pathlib import Path

# Repo root on the path so `common` imports work from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens  # noqa: E402

# Pretend this model has a small window so the demo finishes in 2 seconds.
# (Real windows are 8k-1M+ tokens; a small number makes the shape obvious.)
SIMULATED_WINDOW = 2000

FILLER = (
    "Photosynthesis converts light energy into chemical energy in the "
    "chloroplasts of green plants. "
)


def build_and_grow(window: int) -> None:
    turns: list[dict] = [{"role": "system", "content": "You are a study tutor."}]

    step = 0
    while True:
        step += 1
        turns.append({"role": "user", "content": FILLER * step})
        used = sum(count_tokens(t["content"]) for t in turns)
        print(f"turn {step:>2}  approx tokens used: {used:>5} / {window}")
        if used > window:
            overflow = used - window
            print()
            print(f"OVER BUDGET by {overflow} tokens.")
            print("This is the request that errors out or gets silently truncated.")
            print("The oldest turns are the ones that would be dropped first --")
            print("including, eventually, the system prompt.")
            return


def live_over_budget_request() -> None:
    """Actually send an over-budget request and let the provider say no."""
    from common.llm import DEFAULT_MODEL, chat

    huge = FILLER * 40000  # deliberately far beyond any free model's window
    print(f"sending ~{count_tokens(huge)} tokens to {DEFAULT_MODEL} ...")
    try:
        chat([{"role": "user", "content": huge}], max_retries=1)
        print("unexpected: the request succeeded")
    except Exception as exc:  # noqa: BLE001 - the error IS the lesson
        print("provider said:", str(exc)[:400])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="send a real over-budget request")
    parser.add_argument("--window", type=int, default=SIMULATED_WINDOW)
    args = parser.parse_args()

    if args.live:
        live_over_budget_request()
    else:
        build_and_grow(args.window)
