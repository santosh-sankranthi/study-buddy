# The phases

Each folder below is one phase. Inside, every concept follows the same shape:

```
<concept>/
├── explainer.md   # 1-2 min plain-language explanation, no code
├── demo/          # instructor live-codes this (plainest working version)
├── exercise/      # skeleton for students: same idea, a twist, TODO(n) gaps
└── solution/      # reference answer + check.py self-check
```

Concepts marked *discussion only* have an `explainer.md` and questions in the
phase instructor guide instead of `demo/`.

## Roadmap

| Phase | Folder | Concepts |
|-------|--------|----------|
| 0 | `phase0_fundamentals` | tokens, context_window, training_vs_inference*, sampling |
| 1 | `phase1_prompt_engineering` | system_prompts, few_shot_zero_shot, cot, structured_output, function_calling_concept, react_concept |
| 2 | `phase2_context_engineering` | context_sources, memory, context_compaction, long_context, context_security, mcp* |
| 3 | `phase3_embeddings` | vector_representations, embedding_models, semantic_search |
| 4 | `phase4_vector_databases` | indexing, similarity_search |
| 5 | `phase5_rag` | chunking, embedding, retrieval, generation, rag_evaluation |
| 6 | `phase6_agents` | tools, function_calling, react, agent_loops, multi_agent |
| 7 | `phase7_mcp` | servers, tools_resources, clients, hosts* |
| 8 | `phase8_safety` | prompt_injection, privacy, bias, moderation, adversarial_testing |
| 9 | `phase9_eval_observability` | deterministic_evals, model_based_evals, human_evals, metrics_regression, tracing, production_monitoring |

\* discussion only (no demo/exercise/solution).
