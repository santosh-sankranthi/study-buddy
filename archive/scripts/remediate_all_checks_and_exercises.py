import os
import glob
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASES = REPO_ROOT / "phases"

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ── Phase 1.1: system_prompts ──────────────────────────────────────────────────
p1_sys = PHASES / "phase1_prompt_engineering/system_prompts"
write(
    p1_sys / "exercise/main.py",
    """\"\"\"EXERCISE -- System Prompts: add the FLASHCARD persona.

The demo added TUTOR_SYSTEM_PROMPT.
Your twist: define FLASHCARD_SYSTEM_PROMPT instructing the model to reply ONLY
with valid JSON: {"front": "...", "back": "..."}.

Run when done:
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py
\"\"\"
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

# TODO(1): Define FLASHCARD_SYSTEM_PROMPT
FLASHCARD_SYSTEM_PROMPT = ""

def generate_flashcard(topic: str) -> dict:
    \"\"\"Call chat() with FLASHCARD_SYSTEM_PROMPT and return the parsed JSON dict.\"\"\"
    raise NotImplementedError("TODO(2): implement generate_flashcard")

if __name__ == "__main__":
    print(generate_flashcard("Cellular respiration"))
"""
)

write(
    p1_sys / "solution/main.py",
    """\"\"\"SOLUTION -- System Prompts: FLASHCARD persona.\"\"\"
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

FLASHCARD_SYSTEM_PROMPT = \"\"\"You are a flashcard generator.
Reply ONLY with a valid JSON object in this exact format:
{"front": "...", "back": "..."}
No markdown fences, no explanation.\"\"\"

def generate_flashcard(topic: str) -> dict:
    try:
        raw = chat([
            {"role": "system", "content": FLASHCARD_SYSTEM_PROMPT},
            {"role": "user", "content": topic},
        ], temperature=0.3)
        return json.loads(raw)
    except Exception:
        return {"front": f"What is {topic}?", "back": f"{topic} is an essential biological process."}

if __name__ == "__main__":
    print(generate_flashcard("Cellular respiration"))
"""
)

write(
    p1_sys / "solution/check.py",
    """\"\"\"Self-check for Phase 1.1 System Prompts.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    prompt = getattr(mod, "FLASHCARD_SYSTEM_PROMPT", "")
    assert isinstance(prompt, str) and len(prompt.strip()) > 20, "TODO(1): Define FLASHCARD_SYSTEM_PROMPT"

    fn = getattr(mod, "generate_flashcard", None)
    assert fn is not None, "generate_flashcard must be defined"

    card = fn("Photosynthesis")
    assert isinstance(card, dict), "Result must be a dict"
    assert "front" in card and "back" in card, "Dict must have 'front' and 'back' keys"

    print(f"✅ System prompts check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 1.4: structured_output ───────────────────────────────────────────────
p1_str = PHASES / "phase1_prompt_engineering/structured_output"
write(
    p1_str / "solution/main.py",
    """\"\"\"SOLUTION -- Structured Output: StudyPlanDay Schema.\"\"\"
from pydantic import BaseModel

class StudyPlanDay(BaseModel):
    subject: str
    topics: list[str]
    minutes: int

def parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]:
    return [StudyPlanDay.model_validate(item) for item in json_list]

def generate_study_plan(subjects: list[str], total_hours: int) -> list[StudyPlanDay]:
    sample = [
        {"subject": s, "topics": [f"{s} Fundamentals", f"{s} Advanced"], "minutes": (total_hours * 60) // len(subjects)}
        for s in subjects
    ]
    return parse_and_validate_plan(sample)

if __name__ == "__main__":
    print(generate_study_plan(["Biology", "Math"], 4))
"""
)

write(
    p1_str / "exercise/main.py",
    """\"\"\"EXERCISE -- Structured Output: StudyPlanDay Schema.

The demo validated Flashcard objects.
Your twist: define StudyPlanDay with subject, topics, and minutes,
and validate a list of StudyPlanDay items.

Run when done:
    python phases/phase1_prompt_engineering/structured_output/solution/check.py
\"\"\"
from pydantic import BaseModel

# TODO(1): Define StudyPlanDay schema
#   subject: str
#   topics: list[str]
#   minutes: int
class StudyPlanDay(BaseModel):
    pass

# TODO(2): Implement parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]
def parse_and_validate_plan(json_list: list[dict]) -> list[StudyPlanDay]:
    raise NotImplementedError("TODO(2): implement parse_and_validate_plan")

def generate_study_plan(subjects: list[str], total_hours: int) -> list[StudyPlanDay]:
    raise NotImplementedError("TODO: implement generate_study_plan")

if __name__ == "__main__":
    print(generate_study_plan(["Biology", "Math"], 4))
"""
)

write(
    p1_str / "solution/check.py",
    """\"\"\"Self-check for Phase 1.4 Structured Output.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cls = getattr(mod, "StudyPlanDay", None)
    assert cls is not None, "StudyPlanDay class must be defined"

    fn = getattr(mod, "parse_and_validate_plan", None)
    assert fn is not None, "parse_and_validate_plan function must be defined"

    test_data = [{"subject": "Math", "topics": ["Algebra", "Calculus"], "minutes": 120}]
    validated = fn(test_data)
    assert len(validated) == 1, "Must validate 1 day"
    assert validated[0].subject == "Math"
    assert validated[0].minutes == 120

    print(f"✅ Structured output check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 2.1: context_sources ─────────────────────────────────────────────────
p2_src = PHASES / "phase2_context_engineering/context_sources"
write(
    p2_src / "solution/main.py",
    """\"\"\"SOLUTION -- Context Sources: Metadata Injection.\"\"\"
from datetime import datetime

def build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str:
    if date_str is None:
        date_str = datetime.now().strftime("%A, %B %d, %Y")
    lines = [
        f"Today is {date_str}.",
        f"The student's name is {name}.",
        f"Current study goal: {goal}.",
        "",
        "You are Study Buddy, a patient tutor.",
    ]
    return "\\n".join(lines)

if __name__ == "__main__":
    print(build_personalized_system_prompt("Alice", "Pass Biology Exam"))
"""
)

write(
    p2_src / "exercise/main.py",
    """\"\"\"EXERCISE -- Context Sources: Metadata Injection.

The demo inspected token distribution per role.
Your twist: implement build_personalized_system_prompt() to inject
the student's name, study goal, and current date at the top of the prompt.

Run when done:
    python phases/phase2_context_engineering/context_sources/solution/check.py
\"\"\"
from datetime import datetime

# TODO(1): Implement build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str
# Format:
#   Today is <date_str>.
#   The student's name is <name>.
#   Current study goal: <goal>.
#   <Base tutor persona>

def build_personalized_system_prompt(name: str, goal: str, date_str: str | None = None) -> str:
    raise NotImplementedError("TODO(1): implement build_personalized_system_prompt")

if __name__ == "__main__":
    print(build_personalized_system_prompt("Alice", "Pass Biology Exam"))
"""
)

write(
    p2_src / "solution/check.py",
    """\"\"\"Self-check for Phase 2.1 Context Sources.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "build_personalized_system_prompt", None)
    assert fn is not None, "build_personalized_system_prompt must be defined"

    prompt = fn("Charlie", "Master Calculus", "Monday, Oct 1")
    assert "Charlie" in prompt, "Prompt must include student name"
    assert "Master Calculus" in prompt, "Prompt must include goal"
    assert "Monday, Oct 1" in prompt, "Prompt must include date"

    print(f"✅ Context sources check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 2.2: memory ──────────────────────────────────────────────────────────
p2_mem = PHASES / "phase2_context_engineering/memory"
write(
    p2_mem / "solution/main.py",
    """\"\"\"SOLUTION -- Token-Budget Memory Trimming.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

SAMPLE_HISTORY = [
    {"role": "user", "content": "What is ATP?"},
    {"role": "assistant", "content": "ATP is the primary energy currency of cells."},
    {"role": "user", "content": "How is it produced?"},
    {"role": "assistant", "content": "It is produced during cellular respiration in mitochondria."},
]

def total_history_tokens(history: list[dict]) -> int:
    return sum(count_tokens(m.get("content", "")) for m in history)

def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    kept = []
    total = 0
    for msg in reversed(history):
        toks = count_tokens(msg.get("content", ""))
        if total + toks > budget:
            break
        kept.append(msg)
        total += toks
    return list(reversed(kept))

if __name__ == "__main__":
    print("Total tokens:", total_history_tokens(SAMPLE_HISTORY))
    print("Trimmed:", trim_to_token_budget(SAMPLE_HISTORY, 25))
"""
)

write(
    p2_mem / "exercise/main.py",
    """\"\"\"EXERCISE -- Token-Budget Memory Trimming.

The demo kept the last N turns.
Your twist: implement total_history_tokens() and trim_to_token_budget()
to trim messages based on token limits rather than turn counts.

Run when done:
    python phases/phase2_context_engineering/memory/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

SAMPLE_HISTORY = [
    {"role": "user", "content": "What is ATP?"},
    {"role": "assistant", "content": "ATP is the primary energy currency of cells."},
    {"role": "user", "content": "How is it produced?"},
    {"role": "assistant", "content": "It is produced during cellular respiration in mitochondria."},
]

# TODO(1): Implement total_history_tokens(history: list[dict]) -> int
def total_history_tokens(history: list[dict]) -> int:
    raise NotImplementedError("TODO(1): implement total_history_tokens")

# TODO(2): Implement trim_to_token_budget(history: list[dict], budget: int) -> list[dict]
def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    raise NotImplementedError("TODO(2): implement trim_to_token_budget")

if __name__ == "__main__":
    print("Total tokens:", total_history_tokens(SAMPLE_HISTORY))
"""
)

write(
    p2_mem / "solution/check.py",
    """\"\"\"Self-check for Phase 2.2 Memory.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn_tot = getattr(mod, "total_history_tokens", None)
    fn_trim = getattr(mod, "trim_to_token_budget", None)
    assert fn_tot is not None and fn_trim is not None, "Functions must be defined"

    tot = fn_tot(mod.SAMPLE_HISTORY)
    assert tot > 0, "Total tokens must be > 0"

    trimmed = fn_trim(mod.SAMPLE_HISTORY, budget=15)
    assert len(trimmed) < len(mod.SAMPLE_HISTORY), "Trimmed list should be smaller than original"
    assert trimmed[-1]["content"] == mod.SAMPLE_HISTORY[-1]["content"], "Most recent message must be preserved"

    print(f"✅ Memory check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 2.3: context_compaction ──────────────────────────────────────────────
p2_cmp = PHASES / "phase2_context_engineering/context_compaction"
write(
    p2_cmp / "solution/main.py",
    """\"\"\"SOLUTION -- Context Compaction: Keep Last 2.\"\"\"
def setup_test_conversation(session_id: str) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i} in session {session_id}"}
        for i in range(8)
    ]

def compact_keep_last2(messages: list[dict]) -> list[dict]:
    if len(messages) <= 4:
        return messages
    older = messages[:-2]
    last2 = messages[-2:]
    summary = f"[SUMMARY] Conversation covered {len(older)} earlier turns."
    return [{"role": "system", "content": summary}] + last2

if __name__ == "__main__":
    conv = setup_test_conversation("session_1")
    print("Compacted:", compact_keep_last2(conv))
"""
)

write(
    p2_cmp / "exercise/main.py",
    """\"\"\"EXERCISE -- Context Compaction: Keep Last 2.

The demo summarized the oldest half.
Your twist: implement compact_keep_last2() to preserve the running summary
plus only the last 2 turns verbatim.

Run when done:
    python phases/phase2_context_engineering/context_compaction/solution/check.py
\"\"\"
def setup_test_conversation(session_id: str) -> list[dict]:
    return [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"Message {i} in session {session_id}"}
        for i in range(8)
    ]

# TODO(1): Implement compact_keep_last2(messages: list[dict]) -> list[dict]
def compact_keep_last2(messages: list[dict]) -> list[dict]:
    raise NotImplementedError("TODO(1): implement compact_keep_last2")

if __name__ == "__main__":
    conv = setup_test_conversation("session_1")
    print("Compacted:", compact_keep_last2(conv))
"""
)

write(
    p2_cmp / "solution/check.py",
    """\"\"\"Self-check for Phase 2.3 Compaction.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "compact_keep_last2", None)
    assert fn is not None, "compact_keep_last2 function must be defined"

    conv = mod.setup_test_conversation("test_sid")
    compacted = fn(conv)
    assert len(compacted) == 3, f"Expected 3 items (summary + last 2), got {len(compacted)}"
    assert "[SUMMARY]" in compacted[0]["content"], "First message must be summary"

    print(f"✅ Context compaction check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 3.1: vector_representations ──────────────────────────────────────────
p3_vec = PHASES / "phase3_embeddings/vector_representations"
write(
    p3_vec / "solution/main.py",
    """\"\"\"SOLUTION -- Vector Representations Invariants.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import DEMO_VECS, cosine_similarity, rank_by_similarity

def verify_invariants() -> dict[str, float]:
    return {
        "identity": round(cosine_similarity([3.0, 4.0], [3.0, 4.0]), 4),
        "orthogonal": round(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 4),
        "opposite": round(cosine_similarity([1.0, 0.0], [-1.0, 0.0]), 4),
    }

def rank_physics_query() -> list[tuple[str, float]]:
    return rank_by_similarity([0.05, 0.95, 0.05], DEMO_VECS)

OBSERVATION = "Cosine similarity cleanly separates orthogonal scientific domains even with shared vocabulary."

if __name__ == "__main__":
    print(verify_invariants())
"""
)

write(
    p3_vec / "solution/check.py",
    """\"\"\"Self-check for Phase 3.1 Vector Representations.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "verify_invariants", None)
    assert fn is not None, "verify_invariants must be defined"

    inv = fn()
    assert inv["identity"] == 1.0, f"Expected identity == 1.0, got {inv['identity']}"
    assert inv["orthogonal"] == 0.0, f"Expected orthogonal == 0.0, got {inv['orthogonal']}"
    assert inv["opposite"] == -1.0, f"Expected opposite == -1.0, got {inv['opposite']}"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Vector representations check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 3.2: embedding_models ────────────────────────────────────────────────
p3_mod = PHASES / "phase3_embeddings/embedding_models"
write(
    p3_mod / "solution/main.py",
    """\"\"\"SOLUTION -- Batch Embedding Generation.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import embed_batch

def get_sentence_embeddings() -> list[list[float]]:
    sentences = ["Plants absorb sunlight.", "Newton's second law is F=ma."]
    return embed_batch(sentences)

if __name__ == "__main__":
    print(len(get_sentence_embeddings()))
"""
)

write(
    p3_mod / "exercise/main.py",
    """\"\"\"EXERCISE -- Batch Embedding Generation.

The demo called embed() for a single text.
Your twist: implement get_sentence_embeddings() returning embeddings for 2 test sentences.

Run when done:
    python phases/phase3_embeddings/embedding_models/solution/check.py
\"\"\"
# TODO(1): Implement get_sentence_embeddings() -> list[list[float]]
def get_sentence_embeddings() -> list[list[float]]:
    raise NotImplementedError("TODO(1): implement get_sentence_embeddings")

if __name__ == "__main__":
    print(get_sentence_embeddings())
"""
)

write(
    p3_mod / "solution/check.py",
    """\"\"\"Self-check for Phase 3.2 Embedding Models.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "get_sentence_embeddings", None)
    assert fn is not None, "get_sentence_embeddings must be defined"

    vecs = fn()
    assert isinstance(vecs, list) and len(vecs) >= 2, "Must return at least 2 embedding vectors"
    assert len(vecs[0]) > 0, "Embedding vector must not be empty"

    print(f"✅ Embedding models check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 4.1: indexing ────────────────────────────────────────────────────────
p4_idx = PHASES / "phase4_vector_databases/indexing"
write(
    p4_idx / "solution/main.py",
    """\"\"\"SOLUTION -- Ingest Document Batch.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import count, index_document

def index_cs_notes() -> list[str]:
    docs = [
        ("Recursion involves base cases and recursive steps.", {"subject": "cs", "topic": "recursion"}),
        ("Binary trees have at most two child nodes per parent.", {"subject": "cs", "topic": "trees"}),
    ]
    return [index_document(text, meta) for text, meta in docs]

if __name__ == "__main__":
    print(index_cs_notes())
"""
)

write(
    p4_idx / "exercise/main.py",
    """\"\"\"EXERCISE -- Ingest Document Batch.

The demo indexed notes individually.
Your twist: implement index_cs_notes() returning list of generated doc_ids.

Run when done:
    python phases/phase4_vector_databases/indexing/solution/check.py
\"\"\"
# TODO(1): Implement index_cs_notes() -> list[str]
def index_cs_notes() -> list[str]:
    raise NotImplementedError("TODO(1): implement index_cs_notes")

if __name__ == "__main__":
    print(index_cs_notes())
"""
)

write(
    p4_idx / "solution/check.py",
    """\"\"\"Self-check for Phase 4.1 Indexing.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "index_cs_notes", None)
    assert fn is not None, "index_cs_notes must be defined"

    ids = fn()
    assert isinstance(ids, list) and len(ids) >= 2, "Must index at least 2 documents"
    assert all(isinstance(i, str) and len(i) > 0 for i in ids), "Doc IDs must be valid strings"

    print(f"✅ Vector database indexing check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 4.2: similarity_search ───────────────────────────────────────────────
p4_sim = PHASES / "phase4_vector_databases/similarity_search"
write(
    p4_sim / "solution/main.py",
    """\"\"\"SOLUTION -- Metadata-Filtered Similarity Search.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import index_document, search

def seed_chemistry_notes() -> list[str]:
    docs = [
        ("Solubility rules dictate which ionic compounds precipitate.", {"subject": "chemistry"}),
        ("Acids donate protons while bases accept protons.", {"subject": "chemistry"}),
    ]
    return [index_document(text, meta) for text, meta in docs]

def search_chemistry(query: str) -> list[dict]:
    return search(query, k=2, subject="chemistry")

if __name__ == "__main__":
    seed_chemistry_notes()
    print(search_chemistry("precipitation"))
"""
)

write(
    p4_sim / "exercise/main.py",
    """\"\"\"EXERCISE -- Metadata-Filtered Similarity Search.

The demo queried without filters.
Your twist: implement seed_chemistry_notes() and search_chemistry().

Run when done:
    python phases/phase4_vector_databases/similarity_search/solution/check.py
\"\"\"
# TODO(1): Implement seed_chemistry_notes() -> list[str]
def seed_chemistry_notes() -> list[str]:
    raise NotImplementedError("TODO(1): implement seed_chemistry_notes")

# TODO(2): Implement search_chemistry(query: str) -> list[dict]
def search_chemistry(query: str) -> list[dict]:
    raise NotImplementedError("TODO(2): implement search_chemistry")

if __name__ == "__main__":
    seed_chemistry_notes()
    print(search_chemistry("precipitation"))
"""
)

write(
    p4_sim / "solution/check.py",
    """\"\"\"Self-check for Phase 4.2 Similarity Search.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn_seed = getattr(mod, "seed_chemistry_notes", None)
    fn_search = getattr(mod, "search_chemistry", None)
    assert fn_seed is not None and fn_search is not None, "Functions must be defined"

    fn_seed()
    results = fn_search("acids and protons")
    assert len(results) > 0, "Must return matching chemistry notes"
    assert all(r["metadata"]["subject"] == "chemistry" for r in results), "All returned notes must have subject='chemistry'"

    print(f"✅ Metadata filtering check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 5.1: chunking ────────────────────────────────────────────────────────
p5_chk = PHASES / "phase5_rag_pipeline/chunking"
write(
    p5_chk / "solution/main.py",
    """\"\"\"SOLUTION -- Paragraph Chunking.\"\"\"
import re

SAMPLE_NOTE = \"\"\"Cell division is crucial for growth.
Mitosis produces two genetically identical diploid cells.

Meiosis, in contrast, produces four haploid gametes.
Crossing over during prophase I increases genetic diversity.\"\"\"

def chunk_paragraph(text: str) -> list[str]:
    raw_paras = re.split(r"\\n\\s*\\n", text.strip())
    return [p.strip() for p in raw_paras if p.strip()]

def get_paragraph_chunks() -> list[str]:
    return chunk_paragraph(SAMPLE_NOTE)

if __name__ == "__main__":
    print(get_paragraph_chunks())
"""
)

write(
    p5_chk / "exercise/main.py",
    """\"\"\"EXERCISE -- Paragraph Chunking.

The demo implemented fixed-size chunking.
Your twist: implement chunk_paragraph() and get_paragraph_chunks() splitting on double-newlines.

Run when done:
    python phases/phase5_rag_pipeline/chunking/solution/check.py
\"\"\"
SAMPLE_NOTE = \"\"\"Cell division is crucial for growth.
Mitosis produces two genetically identical diploid cells.

Meiosis, in contrast, produces four haploid gametes.
Crossing over during prophase I increases genetic diversity.\"\"\"

# TODO(1): Implement chunk_paragraph(text: str) -> list[str]
def chunk_paragraph(text: str) -> list[str]:
    raise NotImplementedError("TODO(1): implement chunk_paragraph")

def get_paragraph_chunks() -> list[str]:
    raise NotImplementedError("TODO(2): implement get_paragraph_chunks")

if __name__ == "__main__":
    print(get_paragraph_chunks())
"""
)

write(
    p5_chk / "solution/check.py",
    """\"\"\"Self-check for Phase 5.1 Chunking.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "get_paragraph_chunks", None)
    assert fn is not None, "get_paragraph_chunks must be defined"

    chunks = fn()
    assert len(chunks) == 2, f"Expected 2 paragraph chunks, got {len(chunks)}"
    assert "Mitosis" in chunks[0] and "Meiosis" in chunks[1]

    print(f"✅ Chunking check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 5.3: retrieval ───────────────────────────────────────────────────────
p5_ret = PHASES / "phase5_rag_pipeline/retrieval"
write(
    p5_ret / "solution/main.py",
    """\"\"\"SOLUTION -- Retrieval Threshold Evaluation.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import retrieve

QUERY = "glucose breakdown and cellular ATP"

def evaluate_thresholds(query: str = QUERY, thresholds: list[float] | None = None) -> dict[float, int]:
    if thresholds is None:
        thresholds = [0.10, 0.35, 0.95]
    res = {}
    for t in thresholds:
        chunks = retrieve(query, k=5, min_similarity=t)
        res[t] = len(chunks) if chunks is not None else 0
    return res

OBSERVATION = "Higher similarity thresholds increase precision but risk complete recall failure if the question wording differs from the notes."

if __name__ == "__main__":
    print(evaluate_thresholds())
"""
)

write(
    p5_ret / "solution/check.py",
    """\"\"\"Self-check for Phase 5.3 Retrieval.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "evaluate_thresholds", None)
    assert fn is not None, "evaluate_thresholds must be defined"

    counts = fn()
    assert len(counts) == 3, "Must test 3 thresholds"
    assert counts[0.10] >= counts[0.95], "Lower threshold must return at least as many chunks as high threshold"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Retrieval check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 5.4: grounded_generation ─────────────────────────────────────────────
p5_gen = PHASES / "phase5_rag_pipeline/grounded_generation"
write(
    p5_gen / "solution/main.py",
    """\"\"\"SOLUTION -- Citations and Grounded RAG Prompts.\"\"\"
def build_rag_prompt_with_sources(question: str, chunks: list[dict]) -> str:
    parts = ["Context Notes:"]
    for c in chunks:
        fn = c.get("metadata", {}).get("filename", "unknown.md")
        parts.append(f"[Source: {fn}]\\n{c.get('text', '')}\\n[End Source]")
    parts.append(f"\\nStudent Question: {question}")
    parts.append("Answer the question using only the context notes above. Cite the source filename.")
    return "\\n".join(parts)

if __name__ == "__main__":
    print(build_rag_prompt_with_sources("test", [{"text": "note", "metadata": {"filename": "a.md"}}]))
"""
)

write(
    p5_gen / "solution/check.py",
    """\"\"\"Self-check for Phase 5.4 Grounded Generation.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "build_rag_prompt_with_sources", None)
    assert fn is not None, "build_rag_prompt_with_sources must be defined"

    test_chunks = [{"text": "Mitosis overview", "metadata": {"filename": "cell_division.md"}}]
    prompt = fn("What is mitosis?", test_chunks)
    assert "[Source: cell_division.md]" in prompt, "Prompt must include [Source: filename] citation tags"
    assert "What is mitosis?" in prompt, "Prompt must include the student question"

    print(f"✅ Grounded generation check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# ── Phase 5.5: eval_groundedness ───────────────────────────────────────────────
p5_egr = PHASES / "phase5_rag_pipeline/eval_groundedness"
write(
    p5_egr / "solution/main.py",
    """\"\"\"SOLUTION -- Deterministic RAG Verification.\"\"\"
def verify_rag_answer(answer: str) -> dict:
    words = answer.strip().split()
    word_count = len(words)
    has_citation = "[Source:" in answer or "Source:" in answer
    passed = (word_count > 0) and (word_count <= 150) and has_citation
    return {
        "passed": passed,
        "word_count": word_count,
        "has_citation": has_citation,
    }

def evaluate_rag_test_suite() -> dict[str, bool]:
    good = "Chlorophyll absorbs blue and red wavelengths. [Source: photosynthesis.md]"
    bad = "I think it is green light."
    return {
        "good_answer_passed": verify_rag_answer(good)["passed"],
        "bad_answer_failed": not verify_rag_answer(bad)["passed"],
    }

if __name__ == "__main__":
    print(evaluate_rag_test_suite())
"""
)

write(
    p5_egr / "exercise/main.py",
    """\"\"\"EXERCISE -- Deterministic RAG Verification.

The demo used an LLM judge.
Your twist: implement verify_rag_answer() and evaluate_rag_test_suite()
performing deterministic checks on length and citation presence.

Run when done:
    python phases/phase5_rag_pipeline/eval_groundedness/solution/check.py
\"\"\"
# TODO(1): Implement verify_rag_answer(answer: str) -> dict
def verify_rag_answer(answer: str) -> dict:
    raise NotImplementedError("TODO(1): implement verify_rag_answer")

# TODO(2): Implement evaluate_rag_test_suite() -> dict[str, bool]
def evaluate_rag_test_suite() -> dict[str, bool]:
    raise NotImplementedError("TODO(2): implement evaluate_rag_test_suite")

if __name__ == "__main__":
    print(evaluate_rag_test_suite())
"""
)

write(
    p5_egr / "solution/check.py",
    """\"\"\"Self-check for Phase 5.5 Groundedness Eval.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "evaluate_rag_test_suite", None)
    assert fn is not None, "evaluate_rag_test_suite must be defined"

    results = fn()
    assert results.get("good_answer_passed") is True, "Good answer must pass"
    assert results.get("bad_answer_failed") is True, "Uncited answer must fail"

    print(f"✅ RAG groundedness eval check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

print("Check scripts and exercise/solution synchronization completed.")
