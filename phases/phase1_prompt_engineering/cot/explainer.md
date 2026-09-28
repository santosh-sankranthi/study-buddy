# Chain of Thought (CoT)

## The problem

The tutor answers most questions acceptably, but watch it on a logic puzzle or a
multi-step maths problem: it often jumps to a conclusion that is simply wrong,
with full confidence. Short-circuiting the reasoning process leads to the wrong
answer — and the model can't catch its own mistake because it never wrote down
the intermediate steps.

## How it works (one sentence)

Appending "think step by step" gives the model a scratch pad — it must write out
intermediate reasoning before the final answer, and it cannot skip a step it has
already written down.

## What was broken one increment ago

The tutor persona from Phase 1.1 made the tone consistent but didn't change how
the model *reasons*. A Socratic tutor who gets the maths wrong isn't very helpful.
CoT is the patch for reasoning quality.

## Key intuitions

- The improvement comes from the *written reasoning*, not the phrase "step by
  step". The model is forced to produce a sequence of tokens that represent
  intermediate conclusions — those tokens become the context for the final answer.
- CoT helps most on **multi-step** problems: logic, maths, scheduling, causal
  chains. For simple factual questions it adds length without improving accuracy.
- The `<thinking>` / `<answer>` tags let the app extract the final answer
  separately from the reasoning — the student sees only the answer, but the
  instructor can toggle the reasoning pane to show the chain.
