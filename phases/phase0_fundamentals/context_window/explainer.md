# Context and Context Windows

## The problem

Study Buddy will happily accept a question, then a follow-up, then a whole
pasted chapter. At some point the model simply cannot accept any more: every
model has a **context window**, a maximum number of tokens (input *plus* output)
it can consider in a single call. Past that limit you get an error or silent
truncation -- and a truncation usually drops the *oldest* text, which is exactly
where your system prompt and earliest turns live.

## How it works (one sentence)

The context window is a fixed token budget for one API call: the system prompt,
the entire conversation history, the retrieved documents, and the model's own
reply must all fit inside it, so "how much can I say?" is really "how many tokens
do I have left after everything else?"

## What was broken one increment ago

v0 has no idea how big its inputs are. It will keep appending whatever you send
until the request blows up with an opaque error. Without measuring the window you
cannot decide *what to drop* when things get tight -- which is the seed of the
whole of Phase 2 (context engineering).

## The budget, concretely

```
context window
├── system prompt        (persona / instructions)      <- always keep
├── conversation history (all previous turns)          <- drop oldest first
├── current user turn    (the question just asked)      <- always keep
├── retrieved documents  (notes, later phases)          <- trim by relevance
└── room for the reply   (max_tokens on output)         <- must reserve!
```

The classic mistake is to fill the window with input and leave no room for the
output. Always reserve some budget for the reply.
