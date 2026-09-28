# Training vs Inference

> Discussion-only concept: no demo, no exercise. The instructor talks through
> this for a few minutes and closes with the questions in
> `instructor_guides/phase0_guide.md`.

## The problem

Students often expect the app to "learn" during the lesson -- to remember their
answers, improve when they correct it, or know what happened in the previous
chat. It does none of those things, and understanding *why* prevents a whole
family of misconceptions ("the model got worse today", "it remembered my name
earlier", "can we just fine-tune it on our notes right now?").

## One sentence

**Training** is the expensive, offline process that bakes the model's weights
once, in advance; **inference** is what happens every time you call the API,
where the weights are frozen and the model merely computes an answer from the
tokens you put in the prompt.

## The two phases at a glance

| | Training (pre-training / fine-tuning) | Inference (every API call) |
|---|---|---|
| When | once, offline, in advance | at request time |
| Cost | enormous (GPUs, days, $$$$) | tiny per call, per-token billing |
| Weights | change | frozen |
| What it learns | language, facts, patterns | nothing -- it only *reads* your prompt |
| Latency | hours to weeks | milliseconds to seconds |
| Your data | needs a full retraining run | lives only in the context you send |

## Why this matters for the rest of the workshop

- The model **cannot remember your last conversation** -- if Study Buddy appears
  to, it is because *we* re-sent the history in the prompt (Phase 2, Memory).
- The model **does not learn your notes** by being shown them once. Anything the
  model "knows" must be in the prompt -- not baked into the weights.
- "Can we just fine-tune it on our notes?" is usually the *wrong* first answer:
  fine-tuning is slow, expensive, and does not update when the notes change.
- Nothing you type in the UI persists server-side unless the code explicitly
  saves it.

## Common misconception to pre-empt

"Temperature / prompting 'teaches' the model." No -- those only change *this one
answer*. The weights are identical before and after.
