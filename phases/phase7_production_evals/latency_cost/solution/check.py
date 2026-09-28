"""Self-check -- Latency Cost exercise.

Run:
    python phases/phase7_production_evals/latency_cost/solution/check.py
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

print("Checking latency cost exercise ...\n")

latencies = {
    "embedding": 50.0,
    "retrieval": 15.0,
    "llm_generation": 350.0,
}
metrics = ex.analyze_pipeline_metrics(latencies, "Sample question text", "Sample answer text")

assert metrics["total_latency_ms"] == 415.0, f"Expected 415.0, got {metrics['total_latency_ms']}"
assert metrics["bottleneck_stage"] == "llm_generation"
assert metrics["cost_usd"] > 0
print("✅  analyze_pipeline_metrics correctly computed total latency and identified bottleneck")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
