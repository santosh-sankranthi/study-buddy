"""DEMO -- Latency & Cost Profiling.

Live-code target: profile pipeline stages (prompt assembly vs. generation),
measure elapsed milliseconds, and compute cost metrics for production requests.

Run:
    python phases/phase6_eval_observability/tracing/demo/main.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

print("=" * 60)
print("REQUEST LATENCY & COST PROFILER DEMO")
print("=" * 60)

# Simulate pipeline stage timings
t0 = time.perf_counter()
time.sleep(0.01)  # Stage 1: Prompt assembly (~10ms)
t_prompt = time.perf_counter()

# Stage 2: Generation (simulated prompt tokens & response)
prompt = "Explain cellular respiration concisely."
answer = "Cellular respiration breaks down glucose to produce ATP across glycolysis and oxidative phosphorylation."
time.sleep(0.05)  # Stage 2: LLM generation (~50ms)
t_generation = time.perf_counter()

lat_prompt = round((t_prompt - t0) * 1000, 2)
lat_generation = round((t_generation - t_prompt) * 1000, 2)
lat_total = round((t_generation - t0) * 1000, 2)

in_tok = count_tokens(prompt)
out_tok = count_tokens(answer)
cost = round((in_tok / 1_000_000 * 0.50) + (out_tok / 1_000_000 * 1.50), 6)

print(f"Stage 1: Prompt build:{lat_prompt:>6} ms ({round(lat_prompt / lat_total * 100)}%)")
print(f"Stage 2: Generation:  {lat_generation:>6} ms ({round(lat_generation / lat_total * 100)}%)")
print("-" * 45)
print(f"Total Pipeline Latency: {lat_total:>6} ms")
print(f"Tokens: {in_tok} in, {out_tok} out | Estimated Cost: ${cost:.6f}")
