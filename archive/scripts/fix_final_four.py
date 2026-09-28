from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASES = REPO_ROOT / "phases"

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. Phase 5 Indexing
p5_idx = PHASES / "phase5_rag_pipeline/indexing"
write(
    p5_idx / "exercise/main.py",
    """\"\"\"EXERCISE -- Reusable Note Ingestion Function.

The demo indexed a single note inline.
Your twist: implement index_note_file() as a reusable ingestion function that
accepts raw text and metadata, splits it with chunk_fixed(), indexes each chunk
with {filename, subject, chunk_index, total_chunks}, and returns the list of doc IDs.

Run when done:
    python phases/phase5_rag_pipeline/indexing/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed
from app.vector_store import count, index_document

# TODO(1): Implement index_note_file(text, filename, subject, chunk_size=25, overlap=5) -> list[str]
def index_note_file(
    text: str,
    filename: str,
    subject: str,
    chunk_size: int = 25,
    overlap: int = 5,
) -> list[str]:
    raise NotImplementedError("TODO(1): implement index_note_file")

SAMPLE_NOTE = (
    "Electromagnetism is one of the four fundamental interactions in nature. "
    "It is described by Maxwell's equations, which unify electricity, magnetism, and optics."
)

if __name__ == "__main__":
    print(index_note_file(SAMPLE_NOTE, "electromagnetism.md", "physics"))
"""
)

write(
    p5_idx / "solution/main.py",
    """\"\"\"SOLUTION -- Reusable Note Ingestion Function.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.chunker import chunk_fixed
from app.vector_store import count, index_document

def index_note_file(
    text: str,
    filename: str,
    subject: str,
    chunk_size: int = 25,
    overlap: int = 5,
) -> list[str]:
    chunks = chunk_fixed(text, chunk_size=chunk_size, overlap=overlap)
    doc_ids = []
    for idx, c in enumerate(chunks):
        meta = {
            "filename": filename,
            "subject": subject,
            "chunk_index": idx,
            "total_chunks": len(chunks),
        }
        doc_ids.append(index_document(c, meta))
    return doc_ids

SAMPLE_NOTE = (
    "Electromagnetism is one of the four fundamental interactions in nature. "
    "It is described by Maxwell's equations, which unify electricity, magnetism, and optics."
)

if __name__ == "__main__":
    print(index_note_file(SAMPLE_NOTE, "electromagnetism.md", "physics"))
"""
)

write(
    p5_idx / "solution/check.py",
    """\"\"\"Self-check for Phase 5 Indexing.\"\"\"
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

    fn = getattr(mod, "index_note_file", None)
    assert fn is not None, "index_note_file must be defined"

    sample = "Quantum mechanics governs atomic scales. Uncertainty limits precision."
    ids = fn(sample, "quantum.md", "physics", chunk_size=10, overlap=2)
    assert isinstance(ids, list) and len(ids) >= 1, "Must return list of indexed IDs"

    print(f"✅ Indexing pipeline check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# 2. Phase 6 Agent Safety
p6_as = PHASES / "phase6_agents_and_tools/agent_safety"
write(
    p6_as / "exercise/main.py",
    """\"\"\"EXERCISE -- Multi-Guard Agent Safety Checks.

The demo caught back-to-back loop detection.
Your twist: implement check_agent_safety() evaluating actions against
MAX_STEPS and consecutive-action loop detection.

Run when done:
    python phases/phase6_agents_and_tools/agent_safety/solution/check.py
\"\"\"
# TODO(1): Implement check_agent_safety(actions: list[str], max_steps: int = 5) -> tuple[bool, str, int]
# Returns (halted: bool, reason: str, executed_steps: int)
# reasons: 'done', 'loop_detected', 'max_steps'
def check_agent_safety(actions: list[str], max_steps: int = 5) -> tuple[bool, str, int]:
    raise NotImplementedError("TODO(1): implement check_agent_safety")

# TODO(2): Write observation on deterministic guardrails
OBSERVATION = ""

if __name__ == "__main__":
    seq = ["search_notes('bio')", "search_notes('bio')"]
    print("Result:", check_agent_safety(seq, 5))
"""
)

write(
    p6_as / "solution/main.py",
    """\"\"\"SOLUTION -- Multi-Guard Agent Safety Checks.\"\"\"
def check_agent_safety(actions: list[str], max_steps: int = 5) -> tuple[bool, str, int]:
    last_action = None
    for step, action in enumerate(actions[:max_steps], 1):
        if action == last_action and last_action not in (None, "", "FINISH"):
            return True, "loop_detected", step
        if action.startswith("FINISH"):
            return False, "done", step
        last_action = action
    if len(actions) >= max_steps:
        return True, "max_steps", max_steps
    return False, "done", len(actions)

OBSERVATION = "Deterministic guardrails protect user quota and prevent unbounded inference recursion."

if __name__ == "__main__":
    print(check_agent_safety(["search", "search"]))
"""
)

write(
    p6_as / "solution/check.py",
    """\"\"\"Self-check for Phase 6 Agent Safety.\"\"\"
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

    fn = getattr(mod, "check_agent_safety", None)
    assert fn is not None, "check_agent_safety must be defined"

    halted, reason, steps = fn(["search('bio')", "search('bio')"], 5)
    assert halted is True and reason == "loop_detected", "Consecutive identical calls must trigger loop_detected"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ Agent safety check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# 3. Phase 7 Servers
p7_srv = PHASES / "phase7_mcp/servers"
write(
    p7_srv / "solution/check.py",
    """\"\"\"Self-check for Phase 7.1 MCP Servers.\"\"\"
import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE.parent

class MockServer:
    def __init__(self):
        self.registered = []
    def tool(self):
        def dec(fn):
            self.registered.append(fn.__name__)
            return fn
        return dec

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", action="store_true")
    args = parser.parse_args()

    target_file = (TARGET / "solution" / "main.py") if args.solution else (TARGET / "exercise" / "main.py")
    spec = importlib.util.spec_from_file_location("srv_mod", target_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fn = getattr(mod, "register_grade_tool", None)
    assert fn is not None, "register_grade_tool function must be defined"

    mock = MockServer()
    status = fn(mock)
    assert status is True, "register_grade_tool must return True on success"
    assert "calculate_grade" in mock.registered, "calculate_grade must be registered as a tool"

    print(f"✅ MCP Servers check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

# 4. Phase 8 RAG Isolation
p8_iso = PHASES / "phase8_safety/rag_isolation"
write(
    p8_iso / "exercise/main.py",
    """\"\"\"EXERCISE -- Multi-Chunk Security Sandboxing.

The demo wrapped an individual untrusted chunk.
Your twist: implement build_isolated_context_block(chunks: list[dict]) -> str
to wrap all chunks in unambiguous [RETRIEVED CONTEXT] security boundaries.

Run when done:
    python phases/phase8_safety/rag_isolation/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import wrap_chunk_as_untrusted

# TODO(1): Implement build_isolated_context_block(chunks: list[dict]) -> str
def build_isolated_context_block(chunks: list[dict]) -> str:
    raise NotImplementedError("TODO(1): implement build_isolated_context_block")

# TODO(2): Write observation on prompt isolation
OBSERVATION = ""

if __name__ == "__main__":
    sample = [{"text": "Fact A", "metadata": {"filename": "file_1.md"}}]
    print(build_isolated_context_block(sample))
"""
)

write(
    p8_iso / "solution/main.py",
    """\"\"\"SOLUTION -- Multi-Chunk Security Sandboxing.\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.security import wrap_chunk_as_untrusted

def build_isolated_context_block(chunks: list[dict]) -> str:
    blocks = [
        wrap_chunk_as_untrusted(
            i + 1,
            c["text"],
            c.get("metadata", {}).get("filename", "unknown"),
        )
        for i, c in enumerate(chunks)
    ]
    return "\\n\\n".join(blocks)

OBSERVATION = "Enclosing retrieved text within syntactic data fences instructs the LLM to treat content as untrusted evidence rather than instructions."

if __name__ == "__main__":
    print(build_isolated_context_block([{"text": "Fact", "metadata": {"filename": "f.md"}}]))
"""
)

write(
    p8_iso / "solution/check.py",
    """\"\"\"Self-check for Phase 8 RAG Isolation.\"\"\"
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

    fn = getattr(mod, "build_isolated_context_block", None)
    assert fn is not None, "build_isolated_context_block must be defined"

    sample = [{"text": "Fact text", "metadata": {"filename": "note.md"}}]
    res = fn(sample)
    assert "UNTRUSTED" in res or "RETRIEVED CONTEXT" in res, "Must contain untrusted context boundary tags"
    assert "note.md" in res, "Must include source filename"

    if not args.solution:
        assert getattr(mod, "OBSERVATION", "").strip(), "TODO(2): write observation"

    print(f"✅ RAG isolation check passed ({target_file.name})!")

if __name__ == "__main__":
    main()
"""
)

print("Final four concepts updated successfully.")
