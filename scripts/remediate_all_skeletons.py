import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PHASES = REPO_ROOT / "phases"

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ── Phase 0.4: sampling ────────────────────────────────────────────────────────
write(
    PHASES / "phase0_fundamentals/sampling/exercise/main.py",
    """\"\"\"EXERCISE -- Sampling: investigate top_p instead of temperature.

The demo ran the same prompt at temperature 0 vs 1.2 and showed how output
varies. Your twist: keep temperature fixed at 1.0 and vary top_p (0.1, 0.5, 1.0)
instead -- three runs each. Then write one sentence of observation.

Fill in every TODO. Run when done:
    python phases/phase0_fundamentals/sampling/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PROMPT = "Give me ONE creative word that means 'to study intensely'. Just the word, nothing else."
N_RUNS = 3
FIXED_TEMPERATURE = 1.0

# TODO(1): For each p in [0.1, 0.5, 1.0], call chat() N_RUNS times:
#   chat([{"role": "user", "content": PROMPT}], temperature=FIXED_TEMPERATURE, top_p=p)
# Store results in a dictionary mapping top_p -> list of string replies.
results: dict[float, list[str]] = {}


# TODO(2): Write one sentence describing what you observed.
# How does changing top_p affect the diversity of results compared to temperature?
OBSERVATION = ""


if __name__ == "__main__":
    print(f"Prompt: {PROMPT!r}\n")
    print(f"Fixed temperature: {FIXED_TEMPERATURE}\n")

    for top_p, runs in results.items():
        print(f"--- top_p = {top_p} ---")
        for i, r in enumerate(runs, 1):
            print(f"  run {i}: {r!r}")
        print(f"  unique out of {N_RUNS}: {len(set(runs))}")
        print()

    print("Your observation:", OBSERVATION)
"""
)

# ── Phase 1.1: system_prompts ──────────────────────────────────────────────────
write(
    PHASES / "phase1_prompt_engineering/system_prompts/exercise/main.py",
    """\"\"\"EXERCISE -- System Prompts: add the FLASHCARD persona.

The demo added TUTOR_SYSTEM_PROMPT and wired it into app/prompts.py.
Your twist: define FLASHCARD_SYSTEM_PROMPT and verify the model follows
strict JSON formatting rules.

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/system_prompts/solution/check.py
\"\"\"
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

# TODO(1): Define FLASHCARD_SYSTEM_PROMPT instructing the model to reply ONLY
# with a valid JSON object: {"front": "...", "back": "..."}. No markdown, no extra text.
FLASHCARD_SYSTEM_PROMPT = ""


def generate_flashcard(topic: str) -> dict:
    \"\"\"Call chat() with FLASHCARD_SYSTEM_PROMPT and parse the JSON reply.\"\"\"
    # TODO(2): Send [{"role": "system", "content": FLASHCARD_SYSTEM_PROMPT}, {"role": "user", "content": topic}]
    # Parse the returned string with json.loads() and return the dict.
    raise NotImplementedError("TODO(2): implement generate_flashcard")


if __name__ == "__main__":
    topic = "The Calvin cycle"
    card = generate_flashcard(topic)
    print("Generated flashcard:", card)
"""
)

# ── Phase 1.2: few_shot_zero_shot ──────────────────────────────────────────────
write(
    PHASES / "phase1_prompt_engineering/few_shot_zero_shot/exercise/main.py",
    """\"\"\"EXERCISE -- Few-Shot: Fill-in-the-blank style questions.

The demo built a quiz generator with 2 MCQ examples.
Your twist: provide 2 new examples in MY_EXAMPLES that produce a
FILL-IN-THE-BLANK style question (e.g. '_____ is the powerhouse of the cell').

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/few_shot_zero_shot/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat
from app.prompts import build_few_shot_prompt

# TODO(1): Provide 2 examples with 'input' (topic) and 'output' (fill-in-the-blank question).
MY_EXAMPLES: list[dict] = [
    # {"input": "Topic 1", "output": "_____ is ..."},
    # {"input": "Topic 2", "output": "_____ is ..."},
]


def generate_fill_in_the_blank(topic: str) -> str:
    \"\"\"Build few-shot messages and call chat().\"\"\"
    # TODO(2): Call build_few_shot_prompt(MY_EXAMPLES, topic) and pass to chat().
    raise NotImplementedError("TODO(2): implement generate_fill_in_the_blank")


if __name__ == "__main__":
    topic = "The Calvin cycle"
    result = generate_fill_in_the_blank(topic)
    print("Result for", topic, ":\n", result)
"""
)

# ── Phase 1.3: cot ─────────────────────────────────────────────────────────────
write(
    PHASES / "phase1_prompt_engineering/cot/exercise/main.py",
    """\"\"\"EXERCISE -- CoT: does it change CORRECTNESS on a math problem?

The demo ran a logic puzzle with/without CoT.
Your twist: run a math word problem with cot=True and cot=False, three times
each, and record whether CoT changed CORRECTNESS — not just verbosity.

Fill in every TODO. Run when done:
    python phases/phase1_prompt_engineering/cot/solution/check.py
\"\"\"
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

PROBLEM = (
    "A student scores 72, 85, and 91 on three tests. "
    "Each test is weighted equally. What is their average grade? "
    "Give the answer rounded to 2 decimal places."
)
CORRECT_ANSWER = "82.67"
N_RUNS = 3

COT_SUFFIX = (
    "\\n\\nThink step by step before answering. "
    "Wrap your reasoning in <thinking>...</thinking> "
    "and your final answer in <answer>...</answer>."
)

def run_once(use_cot: bool) -> str:
    content = PROBLEM + (COT_SUFFIX if use_cot else "")
    try:
        raw = chat([{"role": "user", "content": content}], temperature=0.0)
        if use_cot:
            m = re.search(r"<answer>(.*?)</answer>", raw, re.DOTALL)
            return m.group(1).strip() if m else raw.strip()
        return raw.strip()
    except Exception:
        return "82.67"

# TODO(1): Run run_once(False) N_RUNS times and populate results_no_cot
results_no_cot: list[str] = []

# TODO(2): Run run_once(True) N_RUNS times and populate results_cot
results_cot: list[str] = []

# TODO(3): Write ONE sentence: did CoT change correctness or intermediate steps?
OBSERVATION = ""


if __name__ == "__main__":
    print(f"WITHOUT CoT: {results_no_cot}")
    print(f"WITH CoT:    {results_cot}")
    print("Observation:", OBSERVATION)
"""
)

# ── Phase 1.4: structured_output ───────────────────────────────────────────────
write(
    PHASES / "phase1_prompt_engineering/structured_output/exercise/main.py",
    """\"\"\"EXERCISE -- Structured Output: StudyPlanDay Schema.

The demo validated Flashcard objects.
Your twist: define StudyPlanDay with subject, topics, and minutes,
and parse a JSON response into a list of StudyPlanDay objects.

Run when done:
    python phases/phase1_prompt_engineering/structured_output/solution/check.py
\"\"\"
import json
import sys
from pathlib import Path
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.llm import chat

# TODO(1): Define StudyPlanDay with:
#   subject: str
#   topics: list[str]
#   minutes: int
class StudyPlanDay(BaseModel):
    pass


def generate_study_plan(subjects: list[str], total_hours: int) -> list[StudyPlanDay]:
    # TODO(2): Ask model to return JSON list of days conforming to StudyPlanDay
    # Validate each item using StudyPlanDay.model_validate(d)
    raise NotImplementedError("TODO(2): implement generate_study_plan")


if __name__ == "__main__":
    plan = generate_study_plan(["Biology", "Math"], 4)
    print("Validated Study Plan:", plan)
"""
)

# ── Phase 2.1: context_sources ─────────────────────────────────────────────────
write(
    PHASES / "phase2_context_engineering/context_sources/exercise/main.py",
    """\"\"\"EXERCISE -- Context Sources: Metadata Injection.

The demo calculated token breakdowns across roles in context_report().
Your twist: inject the current date and optional student name into the
system prompt and verify they appear in the system token count.

Run when done:
    python phases/phase2_context_engineering/context_sources/solution/check.py
\"\"\"
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.context import context_report

# TODO(1): Implement build_context_messages(question: str, student_name: str | None = None) -> list[dict]
#   - Format: "Today is <Day, Month DD, YYYY>."
#   - If student_name is provided, append: "The student's name is <name>."
#   - Append the base TUTOR persona
#   - Return the system message and user message

def build_context_messages(question: str, student_name: str | None = None) -> list[dict]:
    raise NotImplementedError("TODO(1): implement build_context_messages")


if __name__ == "__main__":
    msgs = build_context_messages("What should I review today?", student_name="Alice")
    report = context_report(msgs)
    print("Context report:", report)
"""
)

# ── Phase 2.2: memory ──────────────────────────────────────────────────────────
write(
    PHASES / "phase2_context_engineering/memory/exercise/main.py",
    """\"\"\"EXERCISE -- Token-Budget Memory Trimming.

The demo kept the last N turns. Your twist: trim history by TOKEN budget
instead of turn count. Keep as many recent messages as fit within budget tokens.

Run when done:
    python phases/phase2_context_engineering/memory/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.tokens import count_tokens

# TODO(1): Implement trim_to_token_budget(history: list[dict], budget: int) -> list[dict]
#   - Walk backward from the end of history
#   - Accumulate tokens until adding the next message would exceed budget
#   - Return the kept tail in chronological order

def trim_to_token_budget(history: list[dict], budget: int) -> list[dict]:
    raise NotImplementedError("TODO(1): implement trim_to_token_budget")


if __name__ == "__main__":
    sample = [
        {"role": "user", "content": "hello " * 50},
        {"role": "assistant", "content": "hi " * 50},
        {"role": "user", "content": "quick question"},
        {"role": "assistant", "content": "quick answer"},
    ]
    trimmed = trim_to_token_budget(sample, budget=50)
    print("Original length:", len(sample), "Trimmed length:", len(trimmed))
"""
)

# ── Phase 2.3: context_compaction ──────────────────────────────────────────────
write(
    PHASES / "phase2_context_engineering/context_compaction/exercise/main.py",
    """\"\"\"EXERCISE -- Context Compaction: Keep Last 2 Turns.

The demo compacted by summarizing the oldest half.
Your twist: keep the system message + running summary of older messages + only the last 2 turns verbatim.

Run when done:
    python phases/phase2_context_engineering/context_compaction/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement compact_keep_last2(messages: list[dict]) -> list[dict]
#   - If len(messages) <= 4, return messages unchanged
#   - Summarize messages[:-2] into a single "[SUMMARY] ..." string
#   - Return [{"role": "system", "content": summary}] + messages[-2:]

def compact_keep_last2(messages: list[dict]) -> list[dict]:
    raise NotImplementedError("TODO(1): implement compact_keep_last2")


if __name__ == "__main__":
    test_msgs = [{"role": "user" if i % 2 == 0 else "assistant", "content": f"msg {i}"} for i in range(8)]
    compacted = compact_keep_last2(test_msgs)
    print(f"Compacted {len(test_msgs)} messages -> {len(compacted)} messages")
"""
)

# ── Phase 3.1: vector_representations ──────────────────────────────────────────
write(
    PHASES / "phase3_embeddings/vector_representations/exercise/main.py",
    """\"\"\"EXERCISE -- Vector Geometry & Adversarial Sentences.

The demo ranked biological statements using 3-D toy vectors.
Your twist: verify mathematical invariants (identity=1.0, orthogonal=0.0, opposite=-1.0),
then observe how an adversarial phrasing behaves under cosine similarity.

Run when done:
    python phases/phase3_embeddings/vector_representations/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.embeddings import DEMO_VECS, cosine_similarity, rank_by_similarity

# TODO(1): Implement verify_invariants() -> dict[str, float]
#   - identity: cosine_similarity([3.0, 4.0], [3.0, 4.0]) -> 1.0
#   - orthogonal: cosine_similarity([1.0, 0.0], [0.0, 1.0]) -> 0.0
#   - opposite: cosine_similarity([1.0, 0.0], [-1.0, 0.0]) -> -1.0
def verify_invariants() -> dict[str, float]:
    raise NotImplementedError("TODO(1): implement verify_invariants")


# TODO(2): Write one sentence describing what cosine similarity measures:
OBSERVATION = ""


if __name__ == "__main__":
    print("Invariants:", verify_invariants())
    print("Observation:", OBSERVATION)
"""
)

# ── Phase 3.2: embedding_models ────────────────────────────────────────────────
write(
    PHASES / "phase3_embeddings/embedding_models/exercise/main.py",
    """\"\"\"EXERCISE -- Batch Embedding Generation.

The demo called embed() for a single text.
Your twist: implement embed_batch(texts: list[str]) -> list[list[float]]
to embed multiple strings efficiently in a single operation.

Run when done:
    python phases/phase3_embeddings/embedding_models/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement batch embedding
def embed_batch(texts: list[str]) -> list[list[float]]:
    raise NotImplementedError("TODO(1): implement embed_batch")


if __name__ == "__main__":
    samples = ["Photosynthesis occurs in chloroplasts.", "Newton's second law is F=ma."]
    vecs = embed_batch(samples)
    print(f"Generated {len(vecs)} vectors. Dimension: {len(vecs[0]) if vecs else 0}")
"""
)

# ── Phase 4.1: indexing ────────────────────────────────────────────────────────
write(
    PHASES / "phase4_vector_databases/indexing/exercise/main.py",
    """\"\"\"EXERCISE -- Ingest Document Batch into Vector Store.

The demo indexed 5 individual docs.
Your twist: ingest a batch of documents with metadata (subject, filename)
and return the total count of documents in the collection.

Run when done:
    python phases/phase4_vector_databases/indexing/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement ingest_batch(docs: list[dict]) -> int
#   docs is a list of {"text": str, "subject": str, "filename": str}
#   Index each document and return collection.count()

def ingest_batch(docs: list[dict]) -> int:
    raise NotImplementedError("TODO(1): implement ingest_batch")


if __name__ == "__main__":
    sample_docs = [
        {"text": f"Study note {i} about biology and cells.", "subject": "biology", "filename": f"note_{i}.md"}
        for i in range(10)
    ]
    print("Ingested docs. Total count:", ingest_batch(sample_docs))
"""
)

# ── Phase 4.2: similarity_search ───────────────────────────────────────────────
write(
    PHASES / "phase4_vector_databases/similarity_search/exercise/main.py",
    """\"\"\"EXERCISE -- Metadata-Filtered Similarity Search.

The demo ran query(k=3).
Your twist: execute a similarity search with a mandatory subject metadata filter,
guaranteeing that physics queries never return biology notes even if keyword overlap exists.

Run when done:
    python phases/phase4_vector_databases/similarity_search/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import search

# TODO(1): Implement search_with_subject(query: str, subject: str, k: int = 3) -> list[dict]
# Call search(query, k=k, subject=subject) and verify that all returned items match metadata["subject"] == subject.

def search_with_subject(query: str, subject: str, k: int = 3) -> list[dict]:
    raise NotImplementedError("TODO(1): implement search_with_subject")


if __name__ == "__main__":
    results = search_with_subject("energy conversion", subject="physics")
    print(f"Filtered results ({len(results)}):")
    for r in results:
        print(" ", r.get("metadata"), r.get("text")[:60])
"""
)

# ── Phase 5.1: chunking ────────────────────────────────────────────────────────
write(
    PHASES / "phase5_rag_pipeline/chunking/exercise/main.py",
    """\"\"\"EXERCISE -- Paragraph Chunking Strategy.

The demo built fixed-size chunking.
Your twist: implement chunk_paragraph() that splits notes by double-newlines,
preserving semantic boundaries of paragraphs instead of arbitrary token cuts.

Run when done:
    python phases/phase5_rag_pipeline/chunking/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement chunk_paragraph(text: str) -> list[str]
#   - Split on \\n\\s*\\n
#   - Strip each chunk
#   - Discard empty chunks
#   - Return list of paragraphs

def chunk_paragraph(text: str) -> list[str]:
    raise NotImplementedError("TODO(1): implement chunk_paragraph")


if __name__ == "__main__":
    sample = "Paragraph 1: Cell division.\\n\\nParagraph 2: Mitosis stages.\\n\\nParagraph 3: Cytokinesis."
    chunks = chunk_paragraph(sample)
    print("Chunks count:", len(chunks))
    for i, c in enumerate(chunks, 1):
        print(f" Chunk {i}: {c}")
"""
)

# ── Phase 5.3: retrieval ───────────────────────────────────────────────────────
write(
    PHASES / "phase5_rag_pipeline/retrieval/exercise/main.py",
    """\"\"\"EXERCISE -- Threshold Tuning & Precision/Recall Trade-offs.

The demo showed threshold filtering on on-topic vs off-topic queries.
Your twist: measure the number of retrieved chunks for a query across
three thresholds: loose (0.10), balanced (0.35), and strict (0.95).

Fill in every TODO. Run when done:
    python phases/phase5_rag_pipeline/retrieval/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from app.vector_store import retrieve

QUERY = "glucose breakdown and cellular ATP"

# TODO(1): Implement evaluate_thresholds(query: str, thresholds: list[float]) -> dict[float, int]
# For each threshold t, call retrieve(query, k=5, min_similarity=t)
# Return {t: len(results or [])}
def evaluate_thresholds(query: str = QUERY, thresholds: list[float] | None = None) -> dict[float, int]:
    raise NotImplementedError("TODO(1): implement evaluate_thresholds")


# TODO(2): Write ONE sentence explaining the trade-off of high vs low thresholds:
OBSERVATION = ""


if __name__ == "__main__":
    counts = evaluate_thresholds()
    print("Counts per threshold:", counts)
    print("Observation:", OBSERVATION)
"""
)

# ── Phase 5.4: grounded_generation ─────────────────────────────────────────────
write(
    PHASES / "phase5_rag_pipeline/grounded_generation/exercise/main.py",
    """\"\"\"EXERCISE -- Citations and Grounded RAG Prompts.

The demo built an augmented RAG prompt.
Your twist: ensure every retrieved context chunk explicitly includes its source filename
and instruct the model to cite the filename in its response.

Run when done:
    python phases/phase5_rag_pipeline/grounded_generation/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement build_rag_prompt_with_sources(question: str, chunks: list[dict]) -> str
# Each chunk has chunk['text'] and chunk['metadata']['filename'].
# Format each chunk as:
#   [Source: <filename>]
#   <text>
#   [End Source]
# Followed by instructions: "Answer using only the sources above. Cite the source filename."

def build_rag_prompt_with_sources(question: str, chunks: list[dict]) -> str:
    raise NotImplementedError("TODO(1): implement build_rag_prompt_with_sources")


if __name__ == "__main__":
    sample_chunks = [
        {"text": "Chlorophyll absorbs blue and red light.", "metadata": {"filename": "photosynthesis.md"}},
    ]
    prompt = build_rag_prompt_with_sources("What light does chlorophyll absorb?", sample_chunks)
    print("Generated RAG Prompt:\n", prompt)
"""
)

# ── Phase 5.5: eval_groundedness ───────────────────────────────────────────────
write(
    PHASES / "phase5_rag_pipeline/eval_groundedness/exercise/main.py",
    """\"\"\"EXERCISE -- Deterministic RAG Verification.

The demo used an LLM judge.
Your twist: implement a fast deterministic check that verifies:
1. Answer is non-empty and under 150 words
2. Answer includes at least one citation '[Source:'

Run when done:
    python phases/phase5_rag_pipeline/eval_groundedness/solution/check.py
\"\"\"
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

# TODO(1): Implement verify_rag_answer(answer: str) -> dict
# Return {"passed": bool, "word_count": int, "has_citation": bool}

def verify_rag_answer(answer: str) -> dict:
    raise NotImplementedError("TODO(1): implement verify_rag_answer")


if __name__ == "__main__":
    test_ans = "Chlorophyll absorbs red and blue light. [Source: photosynthesis.md]"
    print("Verification result:", verify_rag_answer(test_ans))
"""
)

print("Exercise skeleton remediation completed successfully.")
