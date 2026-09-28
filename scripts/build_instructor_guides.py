from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
IG = REPO_ROOT / "instructor_guides"
IG.mkdir(parents=True, exist_ok=True)

def write(filename: str, content: str):
    p = IG / filename
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ── Phase 0 ────────────────────────────────────────────────────────────────────
write(
    "phase0_fundamentals.md",
    """# Phase 0 Instructor Guide: AI & LLM Fundamentals

## Learning Objectives
By the end of Phase 0, students should understand:
1. Models tokenize text into integer IDs, not words or characters.
2. Context windows represent hard limits on total tokens (input + output).
3. Models sample from probability distributions governed by temperature and top_p.
4. LLMs are stateless during inference; in-context learning is not model training.

## Timing & Pacing (Total: 45 min)
- **0.1 Tokens (10 min)**: 2 min explainer, 4 min live demo (`tiktoken`), 4 min exercise.
- **0.2 Context Windows (15 min)**: 2 min explainer, 5 min live demo (context warning), 8 min exercise (budget calculator).
- **0.3 Training vs. Inference (8 min)**: Guided discussion.
- **0.4 Sampling & Temperature (12 min)**: 3 min explainer, 4 min demo (temperature 0 vs 1.5), 5 min exercise (`top_p`).

## Discussion Questions & Model Answers (0.3)
- **Q1: If you tell Study Buddy something wrong five times in a row, has it learned that?**
  - *Model Answer*: No. The model weights are frozen at inference time. It only sees those errors as tokens in the current prompt context. Once the session clears, the model reverts to its base training.
- **Q2: What would you actually have to do to permanently change the model's behavior?**
  - *Model Answer*: Perform weight fine-tuning via gradient descent, or update the model through pre-training/RLHF.

## Common Student Stumbling Blocks
- *Encoding mismatch*: Students trying to use `cl100k_base` methods with unsupported characters.
- *Rate limits on sampling*: Remind students that multiple rapid calls at high temperature can trigger free-tier 429s; backoff is handled automatically by `common/llm.py`.
"""
)

# ── Phase 1 ────────────────────────────────────────────────────────────────────
write(
    "phase1_prompt_engineering.md",
    """# Phase 1 Instructor Guide: Prompt Engineering

## Learning Objectives
1. Understand the role of system prompts in anchoring persona and constraints.
2. Leverage few-shot demonstrations to enforce rigid formatting.
3. Apply Chain of Thought (CoT) to force intermediate reasoning before answers.
4. Validate structured JSON output using Pydantic models.
5. Grasp tool schemas and the ReAct (Reasoning + Acting) execution paradigm.

## Timing & Pacing (Total: 60 min)
- **1.1 System Prompts (10 min)**: Demo Socratic tutor persona; student adds Flashcard persona.
- **1.2 Few-Shot (10 min)**: Demo MCQ generation; student adapts to fill-in-the-blank.
- **1.3 Chain of Thought (10 min)**: Demo reasoning tags `<thinking>`; student runs math word problem.
- **1.4 Structured Output (15 min)**: Demo Pydantic validation on Flashcard; student creates StudyPlanDay.
- **1.5 Function Calling Concept (8 min)**: Demo tool schemas; student adds calculate_grade schema.
- **1.6 ReAct Concept (7 min)**: Trace Thought/Action/Observation on paper/markdown.

## Live-Coding Narration Tips
- Deliberately run the tutor persona without rules, then add: "Never give the answer directly. Ask ONE guiding question." Show the class how the model's behavior flips instantly.
- In 1.4 Structured Output, show a `ValidationError` when a JSON key is missing to illustrate why Pydantic is production-critical.
"""
)

# ── Phase 2 ────────────────────────────────────────────────────────────────────
write(
    "phase2_context_engineering.md",
    """# Phase 2 Instructor Guide: Context Engineering & Memory

## Learning Objectives
1. Quantify token distribution across system, user, assistant, and retrieved data.
2. Build multi-turn conversational memory via session IDs.
3. Prevent context window overflow using sliding-window token trimming and compaction.
4. Understand the latency and cost scaling of long-context stuffing.

## Timing & Pacing (Total: 50 min)
- **2.1 Context Sources (10 min)**: Live demo of `context_report()`; students inject name & date.
- **2.2 Memory (12 min)**: Live demo of session store; students implement token budget trimming.
- **2.3 Context Compaction (12 min)**: Live demo of halving summary; students implement keep-last-2.
- **2.4 Long Context (10 min)**: Demo latency vs document length; students calculate dollar cost.
- **2.5 Context Security (6 min)**: Light sanitizer pass blocking obvious injection strings.

## Common Stumbling Blocks
- *Infinite Session Growth*: Show students what happens when 20 turns are fed back without trimming — point out token counts skyrocketing in the Debug panel.
"""
)

# ── Phase 3 ────────────────────────────────────────────────────────────────────
write(
    "phase3_embeddings.md",
    """# Phase 3 Instructor Guide: Embeddings & Vector Semantics

## Learning Objectives
1. Understand high-dimensional vector representations of text.
2. Implement and verify cosine similarity mathematically without libraries.
3. Transition from hardcoded toy vectors to real embedding models.
4. Execute semantic search by ranking text by vector similarity.

## Timing & Pacing (Total: 45 min)
- **3.1 Vector Representations (15 min)**: Hand-rolled dot product and norms; invariant testing.
- **3.2 Embedding Models (15 min)**: Live API call via `embed()`; students implement `embed_batch()`.
- **3.3 Semantic Search (15 min)**: Ranking candidate sentences against user queries.

## Key Teaching Point
- Contrast keyword search with vector search: "Photosynthesis" and "Plants absorb sunlight" share almost no words, yet their cosine similarity is > 0.85.
"""
)

# ── Phase 4 ────────────────────────────────────────────────────────────────────
write(
    "phase4_vector_databases.md",
    """# Phase 4 Instructor Guide: Vector Databases (ChromaDB)

## Learning Objectives
1. Understand why vector databases are necessary (persistent indexing, HNSW indexing, metadata filtering).
2. Ingest notes and compute document IDs in an embedded ChromaDB collection.
3. Perform similarity queries with strict metadata filters.

## Timing & Pacing (Total: 35 min)
- **4.1 Indexing (15 min)**: Initialize ChromaDB client; index sample notes.
- **4.2 Similarity Search (20 min)**: Query top-k with `where={"subject": "physics"}` filters.

## Common Stumbling Blocks
- Remind students that distance in Chroma with cosine space is $1 - \text{similarity}$. Identical vectors have distance 0.
"""
)

# ── Phase 5 ────────────────────────────────────────────────────────────────────
write(
    "phase5_rag_pipeline.md",
    """# Phase 5 Instructor Guide: Retrieval-Augmented Generation (RAG)

## Learning Objectives
1. Implement document chunking strategies (fixed size with overlap vs paragraph chunking).
2. Wire vector retrieval into augmented prompt generation.
3. Force explicit source citations (`[Source: filename]`) to combat hallucination.
4. Evaluate groundedness deterministically and via LLM-as-a-judge.

## Timing & Pacing (Total: 55 min)
- **5.1 Chunking (12 min)**: Compare fixed-window vs paragraph chunking.
- **5.2 Embedding (3 min)**: Review plumbing reuse.
- **5.3 Retrieval (15 min)**: Implement threshold guard (`min_similarity`).
- **5.4 Generation (15 min)**: Build grounded prompt template with mandatory citations.
- **5.5 RAG Evaluation (10 min)**: Validate answer groundedness and word limits.
"""
)

# ── Phase 6 ────────────────────────────────────────────────────────────────────
write(
    "phase6_agents_and_tools.md",
    """# Phase 6 Instructor Guide: AI Agents & Autonomous Loops

## Learning Objectives
1. Wire Python functions into a callable `TOOL_REGISTRY`.
2. Parse model `tool_calls` payloads and dispatch execution.
3. Implement autonomous ReAct loops with visible think/act/observe trace logging.
4. Enforce strict termination guards: `MAX_STEPS` caps and loop detection.
5. Coordinate multi-agent workflows (Planner, Executor, Critic).

## Timing & Pacing (Total: 60 min)
- **6.1 Tools (10 min)**: Wire `search_notes` and `get_exam_schedule`.
- **6.2 Function Calling Live (12 min)**: Dispatch execution of tool calls.
- **6.3 ReAct Loop (15 min)**: Trace execution through multi-step questions.
- **6.4 Agent Loops (13 min)**: Implement same-tool loop detection.
- **6.5 Multi-Agent Systems (10 min)**: Add Critic verification to Planner/Executor.
"""
)

# ── Phase 7 ────────────────────────────────────────────────────────────────────
write(
    "phase7_mcp.md",
    """# Phase 7 Instructor Guide: Model Context Protocol (MCP)

## Learning Objectives
1. Understand why standardization beats proprietary tool wiring.
2. Build an MCP Server using the official Python SDK exposing tools and resources.
3. Expose static study notes as readable `notes://corpus` resources.
4. Build an MCP Client using `ClientSession` and `stdio_client`.
5. Discuss host security architectures (Claude Desktop, Cursor, local IDEs).

## Timing & Pacing (Total: 45 min)
- **7.1 MCP Servers (15 min)**: Define tools with `@mcp.tool()`; run server standalone.
- **7.2 Tools vs Resources (10 min)**: Differentiate computation tools from data resources.
- **7.3 MCP Clients (15 min)**: Call tools over stdio JSON-RPC.
- **7.4 MCP Hosts (5 min)**: Architecture discussion on security boundaries.
"""
)

# ── Phase 8 ────────────────────────────────────────────────────────────────────
write(
    "phase8_safety.md",
    """# Phase 8 Instructor Guide: AI Safety, Security & Red-Teaming

## Learning Objectives
1. Demonstrate indirect prompt injection via poisoned RAG notes.
2. Neutralize injection using untrusted context fencing (`[RETRIEVED CONTEXT]`).
3. Scrub sensitive PII (emails, phone numbers, credit cards) before inference.
4. Apply two-way content moderation (input and output).
5. Conduct adversarial red-teaming against agent loops and tool dispatchers.

## Timing & Pacing (Total: 50 min)
- **8.1 Prompt Injection (15 min)**: Demonstrate RAG hijack with `injected.md`; apply data fences.
- **8.2 Privacy / PII (10 min)**: Regex scrubbing of international phone numbers and emails.
- **8.3 Bias (8 min)**: Individual observation of demographic framing differences.
- **8.4 Moderation (7 min)**: Two-way input/output moderation checking.
- **8.5 Adversarial Testing (10 min)**: Write tests verifying defense against infinite loops & unauthorized tools.
"""
)

# ── Phase 9 ────────────────────────────────────────────────────────────────────
write(
    "phase9_eval_observability.md",
    """# Phase 9 Instructor Guide: Evaluation & Observability

## Learning Objectives
1. Build deterministic test suites for schema validation and response boundaries.
2. Implement model-based evaluation using LLM-as-a-judge with structured criteria.
3. Calibrate human evaluation rubrics across pedagogical dimensions.
4. Track regression test pass-rate deltas across prompt modifications.
5. Trace per-request latency, token consumption, and dollar costs.
6. Formulate operational production alerts for cost, latency, and groundedness.

## Timing & Pacing (Total: 55 min)
- **9.1 Deterministic Evals (10 min)**: Pytest checks on schema and topics.
- **9.2 Model-Based Evals (12 min)**: LLM judge scoring tone on a 1-5 scale.
- **9.3 Human Evals (10 min)**: Group rubric calibration across 5 samples.
- **9.4 Metrics & Regression (10 min)**: Run 10-item eval suite before/after prompt change.
- **9.5 Tracing & Cost (8 min)**: Analyze span breakdowns from trace reports.
- **9.6 Production Monitoring (5 min)**: Operational alert definitions.
"""
)

print("Created all 10 Instructor Guides successfully.")
