# Phase 0 Instructor Guide: AI & LLM Fundamentals

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
