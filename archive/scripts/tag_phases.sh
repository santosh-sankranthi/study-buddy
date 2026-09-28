#!/usr/bin/env bash
# tag_phases.sh — Create git tags for each phase state and milestone in Study Buddy.

set -e

echo "Creating git tags for Study Buddy curriculum..."

# Base checkpoint
git tag -f v0 -m "v0: Raw one-shot Q&A base"

# Phase 1: Prompt engineering
git tag -f v1 -m "v1: Personas, structured output, reasoning mode"

# Phase 2: Context engineering & memory
git tag -f v2 -m "v2: Named sessions, sliding window memory, compaction"

# Phase 3 & 4: Embeddings & Vector store
git tag -f v3 -m "v3: Embeddings, semantic search, ChromaDB vector store"

# Phase 5: RAG pipeline
git tag -f v4 -m "v4: Grounded generation, citation attribution, hallucination defense"

# Phase 6: Agents & tools
git tag -f v5 -m "v5: Autonomous ReAct loop, tool registry, safety caps, multi-agent"

# Phase 7: MCP & production evals
git tag -f v6 -m "v6: Model Context Protocol server and production evaluations"

# Phase 8: Security & safety
git tag -f v7 -m "v7: Prompt injection firewall, PII scrubbing, output moderation"

# Phase 9: Advanced capstone
git tag -f v8 -m "v8: Complete end-to-end Study Buddy platform"

echo "✅ Created version tags: v0, v1, v2, v3, v4, v5, v6, v7, v8"
