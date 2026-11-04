"""Démonstration du TP 3 : récursivité, Fibonacci, Hanoï et recherche dichotomique."""

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
    print("== Affichages récursifs ==")
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
            f"naïf {naive * 1e3:8.3f} ms | mémoïsé {memoised * 1e6:7.1f} us | "
            f"terminal {terminal * 1e6:7.1f} us"
        )

    print("\n== Maximum par diviser pour régner ==")
    values = [17, 3, 42, 8, 23, 4, 15]
    print(f"max({values}) = {max_list(values)}")

    print("\n== Tours de Hanoï (3 disques) ==")
    for move in hanoi(3):
        print(move)
    print(f"nombre total de déplacements : {len(hanoi(3))} = 2^3 - 1")

    print("\n== Recherche ==")
    sorted_values = [1, 3, 5, 7, 9, 11, 13, 15]
    for target in (1, 7, 15, 8):
        print(
            f"cible {target:>2} : linéaire {linear_search(sorted_values, target):>2}, "
            f"récursive {binary_search_recursive(sorted_values, target):>2}, "
            f"itérative {binary_search_iterative(sorted_values, target):>2}"
        )


if __name__ == "__main__":
    main()
