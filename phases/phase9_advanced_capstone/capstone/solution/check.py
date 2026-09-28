"""Self-check -- Capstone Integration exercise.

Run:
    python phases/phase9_advanced_capstone/capstone/solution/check.py
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

print("Checking Capstone Integration exercise ...\n")

statuses = ex.verify_complete_system()

assert statuses.get("security_input") is True, "Security input layer failed"
assert statuses.get("memory") is True, "Session memory layer failed"
assert statuses.get("context") is True, "Context reporting layer failed"
assert statuses.get("rag") is True, "RAG prompt layer failed"
assert statuses.get("tools") is True, "Tool execution layer failed"
assert statuses.get("moderation") is True, "Output moderation layer failed"
assert statuses.get("all_layers_passed") is True, "Not all system layers passed"
print("✅  All 6 architectural layers verified successfully in end-to-end simulation")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 30
print("✅  Capstone OBSERVATION is documented")

print("\n🎉 CONGRATULATIONS! ALL 10 PHASES OF THE CURRICULUM ARE VERIFIED AND OPERATIONAL!")
