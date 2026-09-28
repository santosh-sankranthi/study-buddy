# Tokens

## The problem

You paste a paragraph into Study Buddy and never think about it again -- but the
model never sees "text". It sees a sequence of **tokens**: small chunks of
characters, usually 3-4 characters of English, sometimes a whole common word,
sometimes half a word. Everything you are billed for, and everything that has to
squeeze through the context window, is counted in tokens, not words or
characters.

If you don't have a feel for tokens, you can't predict three things that matter:

1. **Cost** -- every request is priced per input and output token.
2. **Latency** -- more tokens takes longer to read and generate.
3. **Failure** -- when input + output exceed the context window, the request is
   truncated or rejected, and the app breaks in a way that looks random.

## How it works (one sentence)

A tokenizer is a lookup table learned from data that maps text to a list of
token IDs; common words become one token, rare or new words get split into
pieces, and punctuation/whitespace are their own tokens.

## What was broken one increment ago

Study Buddy v0 sends text to the model raw. It has no idea whether a prompt is
12 tokens or 12,000 -- so it can neither estimate the bill nor notice that a
long question is about to overflow the window. The first thing we need, before
any clever engineering, is the ability to *measure*.

## Key intuition

- Tokens are not words. "Study Buddy" is likely 2-3 tokens; a long unusual
  token can cost several.
- Different models use different tokenizers, so the *same* text can be a
  different number of tokens depending on the model. Never assume one count.
- The practical budgeting rule of thumb: **~1 token is about 0.75 English
  words**, or roughly **100 tokens is about 75 words**.
