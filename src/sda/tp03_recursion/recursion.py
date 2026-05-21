"""Recursive functions of TP 3: displays, Fibonacci and divide and conquer."""

from __future__ import annotations

from collections.abc import Callable, Iterable


def numbers_ascending(n: int) -> list[int]:
    """Return ``[1, 2, ..., n]`` using a recursive definition."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    return numbers_ascending(n - 1) + [n]


def numbers_descending(n: int) -> list[int]:
    """Return ``[n, n-1, ..., 1]`` using a recursive definition."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    return [n] + numbers_descending(n - 1)


def print_ascending(n: int, output: Callable[[int], None] = print) -> None:
    """Display the numbers from 1 to ``n`` in increasing order."""
    if n <= 0:
        return
    print_ascending(n - 1, output)
    output(n)


def print_descending(n: int, output: Callable[[int], None] = print) -> None:
    """Display the numbers from ``n`` to 1 in decreasing order."""
    if n <= 0:
        return
    output(n)
    print_descending(n - 1, output)


def fibonacci1(n: int) -> int:
    """Naive recursive Fibonacci, with ``F(0) = F(1) = 1``.

    The number of calls is exponential: ``T(n) = T(n-1) + T(n-2) + 1``.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return fibonacci1(n - 1) + fibonacci1(n - 2)


def fibonacci2(n: int) -> int:
    """Memoised Fibonacci: each value is computed once (``O(n)``)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    cache: dict[int, int] = {0: 1, 1: 1}

    def fib(k: int) -> int:
        if k not in cache:
            cache[k] = fib(k - 1) + fib(k - 2)
        return cache[k]

    return fib(n)


def fibonacci3(n: int) -> int:
    """Tail-recursive Fibonacci with two accumulators.

    The helper carries ``(F(k), F(k+1))`` as ``(a, b)`` and replaces the pair
    by ``(b, a + b)`` at each call, so the recursion is terminal and uses
    ``O(n)`` time and ``O(1)`` extra arithmetic state.
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    def fib(k: int, a: int, b: int) -> int:
        if k == 0:
            return a
        return fib(k - 1, b, a + b)

    return fib(n, 1, 1)


def max_list(values: Iterable[int]) -> int:
    """Maximum of a list, computed with a divide-and-conquer strategy."""
    items = list(values)
    if not items:
        raise ValueError("max_list() arg is an empty sequence")
    return _max_range(items, 0, len(items))


def _max_range(items: list[int], start: int, end: int) -> int:
    if end - start == 1:
        return items[start]
    middle = (start + end) // 2
    left = _max_range(items, start, middle)
    right = _max_range(items, middle, end)
    return left if left >= right else right
