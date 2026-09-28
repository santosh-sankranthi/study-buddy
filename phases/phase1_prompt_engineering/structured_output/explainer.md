# Structured Output

## The problem

The tutor can now reason step by step, but when Study Buddy needs to produce
data that another part of the system will consume (a JavaScript card renderer,
a scheduler, a database insert), the output must be *machine-readable* JSON —
not "pretty-printed" text that sometimes has trailing commas or is missing a
field. Parsing free text reliably is a solved problem only when the text is
perfectly formatted, which LLMs don't guarantee.

## How it works (one sentence)

We define a Pydantic model, serialise its JSON Schema, pass it as the
`response_format` argument, and validate the model's output with Pydantic before
touching it — so any malformed response raises an exception before it can corrupt
the downstream system.

## What was broken one increment ago

Phase 1.1 asked the flashcard persona to return JSON with a system prompt rule.
It worked most of the time — but "most of the time" means the frontend broke
whenever the model added a markdown fence, a trailing comma, or an extra field.
Structured output via Pydantic is the reliable fix.

## Key intuitions

- **Pydantic is the contract.** The schema enforced by Pydantic is stronger
  than any verbal description in the system prompt.
- **Validate early; crash loudly.** A `ValidationError` on the API response is
  much better than a `KeyError` three layers deep in the frontend.
- **Field validators add domain logic.** `@field_validator("minutes")` catches
  "minutes=-10" before it reaches a database — the model occasionally produces
  nonsense values even when the type is correct.
