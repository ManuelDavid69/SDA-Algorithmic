"""Demonstration of TP 3: recursion, Fibonacci, Hanoi and binary search."""

from __future__ import annotations

import time

from .hanoi import hanoi
from .recursion import (
    fibonacci1,
    fibonacci2,
    fibonacci3,
    max_list,
    numbers_ascending,
    numbers_descending,
)
from .search import binary_search_iterative, binary_search_recursive, linear_search


def main() -> None:
    print("== Recursive displays ==")
    print(f"1..8  : {numbers_ascending(8)}")
    print(f"8..1  : {numbers_descending(8)}")

    print("\n== Fibonacci ==")
    for n in (5, 10, 15, 20, 25, 30):
        start = time.perf_counter()
        value = fibonacci1(n)
        naive = time.perf_counter() - start
        start = time.perf_counter()
        fibonacci2(n)
        memoised = time.perf_counter() - start
        start = time.perf_counter()
        fibonacci3(n)
        terminal = time.perf_counter() - start
        print(
            f"F({n:>2}) = {value:<10} "
            f"naive {naive * 1e3:8.3f} ms | memoised {memoised * 1e6:7.1f} us | "
            f"terminal {terminal * 1e6:7.1f} us"
        )

    print("\n== Divide and conquer maximum ==")
    values = [17, 3, 42, 8, 23, 4, 15]
    print(f"max({values}) = {max_list(values)}")

    print("\n== Towers of Hanoi (3 disks) ==")
    for move in hanoi(3):
        print(move)
    print(f"total moves: {len(hanoi(3))} = 2^3 - 1")

    print("\n== Search ==")
    sorted_values = [1, 3, 5, 7, 9, 11, 13, 15]
    for target in (1, 7, 15, 8):
        print(
            f"target {target:>2}: linear {linear_search(sorted_values, target):>2}, "
            f"recursive {binary_search_recursive(sorted_values, target):>2}, "
            f"iterative {binary_search_iterative(sorted_values, target):>2}"
        )


if __name__ == "__main__":
    main()
