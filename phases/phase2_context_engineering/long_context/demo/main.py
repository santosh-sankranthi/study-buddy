"""DEMO -- Long Context Measurement.

Live-code target: simulate and measure how prompt token size influences
processing overhead, showing the relationship between token count and estimated cost.

Run:
    python phases/phase2_context_engineering/long_context/demo/main.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

SAMPLE_DOC = (
    "Cellular respiration is a metabolic pathway that breaks down glucose and produces ATP. "
    "The stages include glycolysis, pyruvate oxidation, the citric acid cycle, and oxidative phosphorylation. "
    "Mitochondria are the primary sites of ATP production in eukaryotic organisms. "
) * 100

PRICE_PER_M_TOKENS = 0.50  # USD per 1M input tokens

print("=" * 60)
print("LONG CONTEXT IMPACT ANALYSIS")
print("=" * 60)
print(f"{'Target Tokens':>14} | {'Actual Tokens':>14} | {'Est. Cost ($)':>14}")
print("-" * 50)

for multiplier in [5, 15, 30, 60]:
    text_slice = SAMPLE_DOC * multiplier
    tokens = count_tokens(text_slice)
    cost = round((tokens / 1_000_000) * PRICE_PER_M_TOKENS, 6)
    print(f"{multiplier * 100:>14} | {tokens:>14} | ${cost:>13.6f}")

print("-" * 50)
print("Observation: Costs grow linearly with every additional token in context.")
