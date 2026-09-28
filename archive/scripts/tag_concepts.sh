#!/usr/bin/env bash
# tag_concepts.sh — Generate git tags for concepts and version milestones

set -e

echo "Tagging all concepts and phase milestones..."

# Milestone tags
git tag -f v0 -m "v0: Raw one-shot Q&A base"
git tag -f v1 -m "v1: Prompt Engineering"
git tag -f v2 -m "v2: Context Engineering & Memory"
git tag -f v3 -m "v3: Embeddings & Vector Databases"
git tag -f v4 -m "v4: RAG Pipeline Grounded in Student Notes"
git tag -f v5 -m "v5: AI Agents & Autonomous Loops"
git tag -f v6 -m "v6: Model Context Protocol (MCP)"
git tag -f v7 -m "v7: AI Safety & Red-Teaming"
git tag -f v8 -m "v8: Evaluation, Observability & Tracing"

# Concept tags for diffing
CONCEPTS=(
    "p0-tokens"
    "p0-context_window"
    "p0-sampling"
    "p1-system_prompts"
    "p1-few_shot_zero_shot"
    "p1-cot"
    "p1-structured_output"
    "p1-function_calling_concept"
    "p1-react_concept"
    "p2-context_sources"
    "p2-memory"
    "p2-context_compaction"
    "p2-long_context"
    "p2-context_security"
    "p3-vector_representations"
    "p3-embedding_models"
    "p3-semantic_search"
    "p4-indexing"
    "p4-similarity_search"
    "p5-chunking"
    "p5-retrieval"
    "p5-grounded_generation"
    "p5-eval_groundedness"
    "p6-tools"
    "p6-function_calling_live"
    "p6-react_loop"
    "p6-agent_loops"
    "p6-multi_agent"
    "p7-servers"
    "p7-tools_resources"
    "p7-clients"
    "p8-prompt_injection"
    "p8-privacy"
    "p8-bias"
    "p8-moderation"
    "p8-adversarial_testing"
    "p9-deterministic_evals"
    "p9-model_based_evals"
    "p9-human_evals"
    "p9-metrics_regression"
    "p9-tracing"
    "p9-production_monitoring"
)

for c in "${CONCEPTS[@]}"; do
    git tag -f "${c}-exercise" -m "${c} exercise skeleton"
    git tag -f "${c}-demo" -m "${c} instructor demo"
    git tag -f "${c}-solution" -m "${c} reference solution"
done

echo "✅ Created concept tags for ${#CONCEPTS[@]} concepts."
