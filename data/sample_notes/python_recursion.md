# Recursion in Python

A recursive function calls itself on a smaller input until it reaches a **base
case** that returns without recursing. Without a base case you get infinite
recursion and a `RecursionError`.

```python
def factorial(n):
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)   # recursive case
```

Every call adds a **frame** to the call stack, so deep recursion can exhaust
memory. Python's default recursion limit is around 1000 and can be read with
`sys.getrecursionlimit()`. Many recursions can be rewritten as loops to save
stack space. Memoization (caching results, e.g. with `functools.lru_cache`)
turns naive exponential recursions such as Fibonacci into linear ones.
