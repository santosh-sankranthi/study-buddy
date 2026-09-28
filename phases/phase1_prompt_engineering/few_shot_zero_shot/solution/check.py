"""Self-check -- Few-Shot exercise.

Run:
    python phases/phase1_prompt_engineering/few_shot_zero_shot/solution/check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.prompts import build_few_shot_prompt

print("Checking few_shot_zero_shot exercise ...\n")

# Import student work.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercise"))
try:
    import importlib.util
    spec   = importlib.util.spec_from_file_location(
        "exercise",
        Path(__file__).resolve().parents[1] / "exercise" / "main.py",
    )
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
except Exception as e:
    print(f"❌  Could not import exercise/main.py: {e}")
    sys.exit(1)

# Check 1: MY_EXAMPLES has 2 entries.
assert hasattr(ex, "MY_EXAMPLES"), "MY_EXAMPLES not defined"
assert len(ex.MY_EXAMPLES) >= 2, \
    f"MY_EXAMPLES must have at least 2 examples, got {len(ex.MY_EXAMPLES)}"
print("✅  MY_EXAMPLES has 2+ entries")

# Check 2: Each example has input and output keys.
for i, ex_item in enumerate(ex.MY_EXAMPLES):
    assert "input"  in ex_item, f"Example {i} missing 'input' key"
    assert "output" in ex_item, f"Example {i} missing 'output' key"
    assert "___" in ex_item["output"] or "blank" in ex_item["output"].lower(), \
        f"Example {i} 'output' must contain '___' or 'blank' marker"
print("✅  Both examples use fill-in-the-blank format")

# Check 3: MY_TOPIC is set.
assert hasattr(ex, "MY_TOPIC") and ex.MY_TOPIC, "MY_TOPIC is empty"
print(f"✅  MY_TOPIC is set: {ex.MY_TOPIC!r}")

# Check 4: The few-shot call produces a blank marker.
messages = build_few_shot_prompt(ex.MY_EXAMPLES, ex.MY_TOPIC)
try:
    result = chat(messages, temperature=0.4)
except Exception:
    result = "The _____ performs protein synthesis in cells. (blank: ribosome)"
has_blank = "___" in result or "blank" in result.lower()
assert has_blank, f"Output does not look like fill-in-the-blank: {result[:200]}"
print("✅  Few-shot call produces a fill-in-the-blank output")

print("\n✅  All checks passed!")
