"""Self-check -- Deterministic Evals exercise.

Run:
    python phases/phase7_production_evals/evals_deterministic/solution/check.py
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

print("Checking deterministic evals exercise ...\n")

# Valid test
valid_json = '{"question": "What is DNA?", "options": ["Protein", "Nucleic acid", "Lipid", "Carbohydrate"], "correct_index": 1}'
res_valid = ex.eval_quiz_item_deterministic(valid_json)
assert res_valid["all_passed"] is True, f"Valid JSON failed checks: {res_valid}"
print("✅  Valid QuizItem passes all deterministic checks")

# Markdown fence rejection test
res_fences = ex.eval_quiz_item_deterministic(f"```json\n{valid_json}\n```")
assert res_fences["no_fences"] is False and res_fences["all_passed"] is False
print("✅  Markdown fences correctly flagged and failed")

# Bad options count test (3 options instead of 4)
bad_opts = '{"question": "What is DNA?", "options": ["Protein", "Lipid", "Carbohydrate"], "correct_index": 0}'
res_opts = ex.eval_quiz_item_deterministic(bad_opts)
assert res_opts["has_4_options"] is False and res_opts["all_passed"] is False
print("✅  Incorrect option count (3 instead of 4) caught correctly")

# Bad index test (index 4 out of range 0..3)
bad_idx = '{"question": "What is DNA?", "options": ["A", "B", "C", "D"], "correct_index": 4}'
res_idx = ex.eval_quiz_item_deterministic(bad_idx)
assert res_idx["valid_correct_index"] is False and res_idx["all_passed"] is False
print("✅  Out-of-range correct_index caught correctly")

print("\n✅  All checks passed!")
