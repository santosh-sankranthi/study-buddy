# Sampling (and Temperature)

## The problem

Ask Study Buddy the same question twice and you get two different answers. Why
isn't it deterministic? And how do you make it more reliable, or more creative,
without retraining anything? The knobs that control this are the **sampling
parameters**, and temperature is the one you will use most.

## How it works (one sentence)

At each step the model produces a probability for every possible next token; the
sampling parameters decide how that probability distribution gets turned into an
actual pick -- `temperature` flattens it (more random) or sharpens it (more
deterministic), and `top_p` restricts the pick to the most likely tokens whose
probabilities sum to p.

## What was broken one increment ago

Every concept so far has been about *reading* the model. This is the first knob
that changes the *output* -- and the app currently exposes none of it. The
practical bug: identical prompts give different answers, so nothing is
reproducible and the tutor's tone drifts from run to run. Until you can turn the
randomness down, you cannot test anything.

## The knobs

- **temperature** (0 to 2): 0 is nearly deterministic (always the most likely
  token); ~0.7 is a normal conversational default; 1.2+ gets creative and
  unreliable. It does not *mean* "creativity", it means "how much to reshape the
  distribution before sampling".
- **top_p** (nucleus sampling, 0 to 1): keep only the smallest set of tokens
  whose probabilities add up to p, then sample within that set. `top_p=1` means
  no filtering; `top_p=0.1` means "only consider the very likeliest tokens".
- **Rule of thumb:** change *either* temperature *or* top_p in a given
  experiment, not both, or you cannot tell which one did what.
- **Even temperature 0 is not guaranteed identical** across calls on hosted
  models (batching and GPU non-determinism), but it is far more stable.
