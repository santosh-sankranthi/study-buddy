# Few-Shot / Zero-Shot Learning

## The problem

After Phase 1.1, Study Buddy has a persona — but when you ask it to produce
output in a specific *format* (a quiz question, a summary with bullet points,
a multiple-choice item), a verbal description alone is often unreliable. The
model produces roughly correct content in the wrong shape. You would need to
write an increasingly detailed prompt just to nail the format every time.

## How it works (one sentence)

Few-shot learning adds 2–5 worked examples to the prompt — each example shows
the model exactly what input should produce exactly what output — so the model
activates learned patterns instead of trying to infer your format from a
description.

## What was broken one increment ago

The flashcard and quiz-item system prompts from Phase 1.1 describe the desired
output format in words. That works some of the time, but complex formats (e.g.
"a multiple-choice question with exactly 4 options, one marked correct, in a
specific JSON shape") are much more reliably produced by showing 2 examples than
by describing them.

## Key intuitions

- **Examples beat descriptions.** "Here is what it should look like: input →
  output" is clearer to a model than "the output should be structured as...".
- **Fewer, higher-quality examples beat many mediocre ones.** 2 clean examples
  outperform 10 inconsistent ones.
- Zero-shot = just the instruction. Few-shot = instruction + examples. The
  quality jump from 0 to 2 examples is usually larger than from 2 to 10.
- The examples also implicitly constrain the response length, tone, and format.
