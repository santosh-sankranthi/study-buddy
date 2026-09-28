# Phase 2 Instructor Guide: Context Engineering & Memory

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
