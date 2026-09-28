"""Self-check -- Output Moderation exercise.

Run:
    python phases/phase8_security_safety/output_moderation/solution/check.py
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

print("Checking output moderation exercise ...\n")

# Safe text test
safe_text = "Mitochondria convert glucose to ATP."
deliv_safe, blocked_safe = ex.filter_safe_response(safe_text)
assert blocked_safe is False
assert deliv_safe == safe_text
print("✅  Safe educational output delivered unhindered")

# Unsafe text test
unsafe_text = "Threatening violence and attack with a bomb weapon."
deliv_unsafe, blocked_unsafe = ex.filter_safe_response(unsafe_text)
assert blocked_unsafe is True
assert deliv_unsafe == ex.SAFE_REFUSAL
print("✅  Harmful output successfully blocked and replaced with standardized safe refusal")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
