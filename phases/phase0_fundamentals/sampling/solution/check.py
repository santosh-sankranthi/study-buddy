"""Self-check for Sampling exercise.

Run from the repo root:
    python phases/phase0_fundamentals/sampling/solution/check.py
    python phases/phase0_fundamentals/sampling/solution/check.py --solution
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

parser = argparse.ArgumentParser()
parser.add_argument("--solution", action="store_true", help="Check reference solution instead of exercise.")
args = parser.parse_args()

if args.solution:
    from phases.phase0_fundamentals.sampling.solution.main import OBSERVATION, results
else:
    from phases.phase0_fundamentals.sampling.exercise.main import OBSERVATION, results

print("Checking sampling exercise ...\n")

# ── Check 1: results dict has the right keys
assert set(results.keys()) == {0.1, 0.5, 1.0}, \
    f"results dict must have keys 0.1, 0.5, 1.0. Got: {set(results.keys())}"
print("✅  results dict has correct top_p keys")

# ── Check 2: each key maps to a list of N_RUNS strings
for top_p, runs in results.items():
    assert isinstance(runs, list), f"results[{top_p}] must be a list, got {type(runs)}"
    assert len(runs) == 3, f"results[{top_p}] must have 3 runs, got {len(runs)}"
    assert all(isinstance(r, str) and r.strip() for r in runs), \
        f"All runs for top_p={top_p} must be non-empty strings"
print("✅  each top_p has exactly 3 non-empty result strings")

# ── Check 3: OBSERVATION is filled in
assert isinstance(OBSERVATION, str) and len(OBSERVATION.strip()) > 20, \
    "OBSERVATION must be a non-empty string (> 20 chars). Did you fill in TODO(2)?"
print("✅  OBSERVATION is filled in")

print("\n✅  All checks passed! Great work.")
