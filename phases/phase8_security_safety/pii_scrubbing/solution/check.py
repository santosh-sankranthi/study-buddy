"""Self-check -- PII Scrubbing exercise.

Run:
    python phases/phase8_security_safety/pii_scrubbing/solution/check.py
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

print("Checking PII scrubbing exercise ...\n")

sample = "Reach out via student@cambridge.edu or text +91 9876543210 or call +44 2079460999."
clean, types = ex.audit_pii_content(sample)

assert "student@cambridge.edu" not in clean, "Email was not redacted"
assert "[EMAIL_REDACTED]" in clean
assert "EMAIL" in types
print("✅  Email address correctly identified and redacted")

assert "+91 9876543210" not in clean, "India phone number was not redacted"
assert "[PHONE_IN_REDACTED]" in clean or "PHONE_IN" in types
print("✅  Indian phone number correctly identified and redacted")

assert "+44 2079460999" not in clean, "UK phone number was not redacted"
assert "[PHONE_UK_REDACTED]" in clean or "PHONE_UK" in types
print("✅  UK phone number correctly identified and redacted")

assert hasattr(ex, "OBSERVATION") and len(ex.OBSERVATION.strip()) > 20
print("✅  OBSERVATION is documented")

print("\n✅  All checks passed!")
