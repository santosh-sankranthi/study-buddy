"""Self-check -- Long Context exercise.

Run:
    python phases/phase2_context_engineering/long_context/solution/check.py
"""

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

spec = importlib.util.spec_from_file_location(
    "ex", Path(__file__).resolve().parents[1] / "exercise" / "main.py"
)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

print("Checking long context exercise ...\n")

# Test calculate_cost
cost = ex.calculate_cost(input_tokens=1_000_000, output_tokens=1_000_000, price_per_m_input=0.50, price_per_m_output=1.50)
assert cost == 2.0, f"Expected 2.0, got {cost}"
print("✅  calculate_cost calculates exact price correctly")

# Test 10-turn modeling
cost_10k = ex.model_10_turn_session(10_000)
cost_100k = ex.model_10_turn_session(100_000)
assert cost_100k > cost_10k * 8, "Cost should scale with doc token size"
print(f"✅  10-turn session modeling scales properly (${cost_10k:.4f} vs ${cost_100k:.4f})")

# Test observation
assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 30
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
