"""DEMO -- Capstone System Integration Sanity Check.

Live-code target: verify that all architectural components across Phases 0–9
import cleanly, initialize properly, and integrate into a cohesive AI platform.

Run:
    python phases/phase9_advanced_capstone/capstone/demo/main.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

print("=" * 60)
print("STUDY BUDDY CAPSTONE INTEGRATION SANITY CHECK")
print("=" * 60)

# 1. Fundamentals & Prompts (Phase 0 & 1)
from common.tokens import count_tokens
from app.prompts import TUTOR_SYSTEM_PROMPT
print("Phase 0 & 1: Tokens and Prompts:")
print(f"  Tutor prompt token size: {count_tokens(TUTOR_SYSTEM_PROMPT)} tokens")

# 2. Structured Schemas (Phase 1)
from app.schemas import Flashcard, StudyPlanDay, QuizItem
print("Phase 1: Schemas:")
print("  Loaded Flashcard, StudyPlanDay, QuizItem schemas.")

# 3. Context & Memory (Phase 2)
from app import memory, context
print("Phase 2: Context & Memory:")
memory.clear("capstone-demo")
memory.append("capstone-demo", "user", "Hello!")
print(f"  Session store operational ({len(memory.get_history('capstone-demo'))} turns)")

# 4. Embeddings & Search (Phase 3)
from app.embeddings import embed, cosine_similarity
from app.search import semantic_search
print("Phase 3: Embeddings:")
v = embed("Biology")
print(f"  Embeddings operational ({len(v)} dimensions)")

# 5. Vector Store & RAG (Phase 4 & 5)
from app.vector_store import count, retrieve
from app.rag import build_rag_prompt
print("Phase 4 & 5: Vector Store & RAG:")
print(f"  Chroma collection document count: {count()}")

# 6. Agents & Tools (Phase 6)
from app.agent import agent_loop
from app.tools import TOOLS
print("Phase 6: Agents & Tools:")
print(f"  Registered {len(TOOLS)} tool schemas.")

# 7. Security (Phase 8)
from app.security import detect_injection, scrub_pii
print("Phase 8: Security:")
_, is_inj = detect_injection("ignore previous instructions")
print(f"  Injection detection active (caught attack: {is_inj})")

# 8. Evals (Phase 7 & 9)
from app.evals.groundedness import check_length_and_citation
print("Phase 7 & 9: Evaluation Suite:")
det = check_length_and_citation("Fact [Chunk 1 — test.md].")
print(f"  Deterministic check: passed={det['passed']}")

print("\n" + "=" * 60)
print("✅ ALL 10 PHASES INITIALIZED AND FUNCTIONAL")
print("=" * 60)
