import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASES = REPO_ROOT / "phases"

def rename_dir(old_rel, new_rel):
    old_p = PHASES / old_rel
    new_p = PHASES / new_rel
    if old_p.exists() and not new_p.exists():
        new_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old_p), str(new_p))
        print(f"Renamed: {old_rel} -> {new_rel}")
    elif old_p.exists() and new_p.exists():
        print(f"Both exist: {old_rel} and {new_rel}")

# 1. Phase 2 renaming
rename_dir("phase2_context_engineering/context_injection", "phase2_context_engineering/context_sources")
rename_dir("phase2_context_engineering/session_memory", "phase2_context_engineering/memory")
rename_dir("phase2_context_engineering/prompt_injection", "phase2_context_engineering/context_security")

# 2. Phase 3 renaming
rename_dir("phase3_embeddings/vector_math", "phase3_embeddings/vector_representations")
rename_dir("phase3_embeddings/embedding_api", "phase3_embeddings/embedding_models")

# 3. Phase 4 renaming
rename_dir("phase4_vector_databases/vector_db_basics", "phase4_vector_databases/indexing")
rename_dir("phase4_vector_databases/metadata_filtering", "phase4_vector_databases/similarity_search")

# 4. Phase 9 removal of hallucinated capstone
capstone_p = PHASES / "phase9_advanced_capstone"
if capstone_p.exists():
    shutil.rmtree(str(capstone_p))
    print("Removed hallucinated phase9_advanced_capstone")

# 5. Move phase7_production_evals to phase9_eval_observability
p7_prod = PHASES / "phase7_production_evals"
p9_eval = PHASES / "phase9_eval_observability"
if p7_prod.exists() and not p9_eval.exists():
    shutil.move(str(p7_prod), str(p9_eval))
    print("Moved phase7_production_evals -> phase9_eval_observability")

# Rename concepts inside phase9_eval_observability
rename_dir("phase9_eval_observability/evals_deterministic", "phase9_eval_observability/deterministic_evals")
rename_dir("phase9_eval_observability/llm_as_judge", "phase9_eval_observability/model_based_evals")
rename_dir("phase9_eval_observability/regression_testing", "phase9_eval_observability/metrics_regression")
rename_dir("phase9_eval_observability/latency_cost", "phase9_eval_observability/tracing")

# 6. Transform phase8_security_safety -> phase8_safety
p8_sec = PHASES / "phase8_security_safety"
p8_safe = PHASES / "phase8_safety"
if p8_sec.exists() and not p8_safe.exists():
    shutil.move(str(p8_sec), str(p8_safe))
    print("Moved phase8_security_safety -> phase8_safety")

rename_dir("phase8_safety/prompt_injection_advanced", "phase8_safety/prompt_injection")
rename_dir("phase8_safety/pii_scrubbing", "phase8_safety/privacy")
rename_dir("phase8_safety/output_moderation", "phase8_safety/moderation")

# Create phase7_mcp directory
(PHASES / "phase7_mcp").mkdir(parents=True, exist_ok=True)
(PHASES / "phase7_mcp" / "__init__.py").touch()

print("Phase structure remediation completed successfully.")
