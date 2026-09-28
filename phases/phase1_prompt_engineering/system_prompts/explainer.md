# System Prompts

## The problem

Open Study Buddy v0 and ask it "What is photosynthesis?" — then ask it again.
The answers will differ in tone, length, structure, and voice. Sometimes it
sounds like a textbook; sometimes it lectures; sometimes it just lists facts.
There is no *Study Buddy* — just a raw language model doing its best guess at
what to say. Students need consistency and a clear teaching personality before
they can trust the tool.

## How it works (one sentence)

The system prompt is a message you prepend to every conversation — before any
user input — that tells the model who it is, what its job is, and what rules it
must follow.

## What was broken one increment ago

v0's `/ask` endpoint passed a single user message with no system prompt, so the
model had no persona, no constraints, and no consistent voice. Every response was
a roll of the dice in terms of tone and format.

## Key intuitions

- The system prompt is **not** privileged at the model level — it is just the
  first message, tagged `"role": "system"`. The model was fine-tuned to follow
  system prompts, but it is not technically impossible to override them (that is
  the whole problem with prompt injection, which Phase 8 addresses).
- **Specificity beats length.** A 3-line system prompt with concrete rules
  ("keep replies under 4 sentences", "end with an encouraging phrase") beats a
  2-page philosophical description of who the tutor should be.
- Changing the system prompt is the cheapest, fastest way to change the model's
  behaviour across *all* users simultaneously — no retraining, no deployment.
