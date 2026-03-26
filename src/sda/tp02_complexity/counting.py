"""Elementary operation counting for the five programs of TP 2, exercise 1.

The course ignores the loop-control instructions (``range`` and the test that
keeps the loop variable in range).  We therefore count one operation per
executed assignment / arithmetic line, which is enough to identify the
asymptotic class.  Every function also returns the final value of the program
so that the loop can be checked against its closed form.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Count:
    """Number of elementary operations and final value of a program."""

    operations: int
    value: int


def program1(n: int) -> Count:
    """Two independent loops of ``n`` iterations: ``T(n) = 2n + 1``."""
    if n < 0:
        raise ValueError("n must be non-negative")
    test = 0  # 1 operation
    operations = 1
    for _ in range(n):
        test = test + 1
    operations += n
    for _ in range(n):
        test = test - 1
    operations += n
    return Count(operations, test)


def program2(n: int) -> Count:
    """Two nested loops: ``T(n) = n^2 + 1``."""
    if n < 0:
        raise ValueError("n must be non-negative")
    test = 0  # 1 operation
    operations = 1
    for i in range(n):
        for j in range(n):
            test = test + i * j
    operations += n * n
    return Count(operations, test)


def program3(n: int) -> Count:
    """Three operations in the double loop, three in the simple loop.

    ``T(n) = 3n^2 + 3n + 3``.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b, c = 5, 6, 10  # 3 operations
    d = 33
    operations = 3
    for i in range(n):
        for j in range(n):
            x = i * i
            y = j * j
            z = i * j
            _ = (x, y, z)
    operations += 3 * n * n
    for k in range(n):
        w = a * k + 45
        v = b * b
        d = 33
        _ = (w, v, d)
    operations += 3 * n
    return Count(operations, d)


def program4(n: int) -> Count:
    """Halving loop: ``floor(log2 n) + 1`` iterations, two operations each."""
    if n < 0:
        raise ValueError("n must be non-negative")
    i = n  # 1 operation
    operations = 1
    while i > 0:
        k = 2 + 2
        i = i // 2
        _ = k
        operations += 2
    return Count(operations, k if n > 0 else 0)


def program5(n: int) -> Count:
    """Triple loop with a constant inner loop.

    ``T(n) = 1 + 6 * (1 + 2 + ... + n^2) = 3n^2(n^2 + 1) + 1``.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    total = 0  # 1 operation
    operations = 1
    for i in range(1, n * n + 1):
        for _ in range(1, i + 1):
            for _ in range(1, 7):
                total = total + 1
    operations += 6 * n * n * (n * n + 1) // 2
    return Count(operations, total)


def program1_formula(n: int) -> int:
    return 2 * n + 1


def program2_formula(n: int) -> int:
    return n * n + 1


def program3_formula(n: int) -> int:
    return 3 * n * n + 3 * n + 3


def program4_formula(n: int) -> int:
    if n == 0:
        return 1
    return 1 + 2 * (n.bit_length())  # floor(log2 n) + 1 iterations


def program5_formula(n: int) -> int:
    return 3 * n * n * (n * n + 1) + 1
