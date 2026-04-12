"""Demonstration of TP 4: sorting algorithms and candy distribution."""

from __future__ import annotations

import random
import time

from .candies import best_distribution, brute_force
from .merge import merge_sort
from .selection import selection_sort
from .thirds import thirds_sort


def main() -> None:
    random.seed(20251006)
    values = [random.randint(0, 99) for _ in range(20)]
    print(f"input          : {values}")
    print(f"selection sort : {selection_sort(list(values))}")
    print(f"merge sort     : {merge_sort(values)}")
    print(f"two-thirds sort: {thirds_sort(list(values))}")

    print("\n== Runtime on 400 elements ==")
    large = [random.randint(0, 1000) for _ in range(400)]
    for name, algorithm in (
        ("selection", selection_sort),
        ("merge", merge_sort),
        ("two-thirds", thirds_sort),
    ):
        start = time.perf_counter()
        algorithm(list(large))
        elapsed = time.perf_counter() - start
        print(f"{name:>11}: {elapsed * 1e3:8.2f} ms")

    print("\n== Candy distribution ==")
    packets = [7, 3, 2, 9, 12, 5, 8, 4]
    children = 3
    print(f"packets: {packets}, children: {children}")
    difference, choice = brute_force(packets, children)
    print(f"brute force : difference {difference}, choice {choice}")
    difference, choice = best_distribution(packets, children)
    print(f"sliding window: difference {difference}, choice {choice}")


if __name__ == "__main__":
    main()
