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
| 2 | `phase2_context_engineering` | context_sources, memory, context_compaction, long_context, context_security, mcp_concept* |
| 3 | `phase3_embeddings` | vector_representations, embedding_models, semantic_search |
| 4 | `phase4_vector_databases` | indexing, similarity_search |
| 5 | `phase5_rag_pipeline` | chunking, embedding*, indexing, retrieval, grounded_generation, eval_groundedness |
| 6 | `phase6_agents_and_tools` | tools, function_calling_live, react_loop, agent_loops, agent_safety, multi_agent |
| 7 | `phase7_mcp` | servers, tools_resources, clients, hosts* |
| 8 | `phase8_safety` | prompt_injection, rag_isolation, privacy, bias, moderation, adversarial_testing |
| 9 | `phase9_eval_observability` | deterministic_evals, model_based_evals, human_evals, metrics_regression, tracing, production_monitoring |

\* discussion only (no demo/exercise/solution).

## Running the self-checks

Each `solution/check.py` is a standalone script, but the repo root
`conftest.py` also lets pytest collect them all:

```bash
pytest                  # fast, offline checks against the reference solutions
pytest --run-llm-checks # include the checks that call the model
```
