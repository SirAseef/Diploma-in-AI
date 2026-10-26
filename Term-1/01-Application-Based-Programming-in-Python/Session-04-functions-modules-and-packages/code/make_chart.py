"""Count calls of naive vs cached Fibonacci -> ../images/fibonacci_calls.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def naive_calls(n):
    calls = 0
    def fib(k):
        nonlocal calls
        calls += 1
        return k if k < 2 else fib(k - 1) + fib(k - 2)
    fib(n)
    return calls

def cached_calls(n):
    calls, memo = 0, {}
    def fib(k):
        nonlocal calls
        calls += 1
        if k in memo:
            return memo[k]
        memo[k] = k if k < 2 else fib(k - 1) + fib(k - 2)
        return memo[k]
    fib(n)
    return calls

ns = list(range(1, 26))
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.plot(ns, [naive_calls(n) for n in ns], "o-", label="naive recursion", color="#c62828")
ax.plot(ns, [cached_calls(n) for n in ns], "s-", label="with cache (memoisation)", color="#2e7d32")
ax.set_yscale("log"); ax.set_xlabel("n"); ax.set_ylabel("function calls (log scale)")
ax.set_title("Calls needed to compute fib(n)"); ax.legend(); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig("../images/fibonacci_calls.png", dpi=120)
print("naive fib(25) calls:", naive_calls(25), "| cached:", cached_calls(25))
