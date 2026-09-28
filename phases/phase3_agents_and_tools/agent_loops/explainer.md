# 3.4 — Agent Loops & Termination Guards

## What was broken before
A single ReAct step is not an autonomous agent — the model must be allowed to iterate in a loop until it reaches a conclusion (`FINISH`). However, autonomous loops risk infinite loops, rapid token depletion, and huge API bills if the model repeats the same action over and over.

## How it works
An agent loop wraps tool execution in a bounded loop (`while not done:` or `for step in range(MAX_STEPS):`). We implement two critical safety guards:
1. A hard iteration cap (`MAX_STEPS = 10`)
2. Same-tool-twice loop detection (halting if the exact same tool and arguments are executed back-to-back).
