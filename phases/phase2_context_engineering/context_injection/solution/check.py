"""Self-check -- Context Injection exercise.

Run:
    python phases/phase2_context_engineering/context_injection/solution/check.py
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

print("Checking context injection exercise ...\n")

# Check personalized prompt
p = ex.build_personalized_system_prompt("Charlie", "Master Calculus", "Monday, Oct 1")
assert "Charlie" in p, "Expected student name in prompt"
assert "Master Calculus" in p, "Expected study goal in prompt"
assert "Monday, Oct 1" in p, "Expected date in prompt"
print("✅  build_personalized_system_prompt contains all injected metadata")

# Check session payload and context report
payload = ex.create_session_payload("How do limits work?", "Charlie", "Master Calculus")
report = payload["context_report"]
assert "system" in report and "user" in report and "total" in report
assert report["system"] > 30, "System tokens should include base prompt and metadata"
assert report["total"] >= report["system"] + report["user"]
print("✅  context_report accurately tracks injected metadata tokens")

print("\n✅  All checks passed!")
