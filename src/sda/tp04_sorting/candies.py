"""Candy distribution problem (TP 4, exercise 4).

Given ``n`` packets of candies and ``m`` children, choose exactly ``m``
packets so that the difference between the largest and the smallest chosen
packet is minimal.
"""

from __future__ import annotations

from itertools import combinations
from typing import Sequence


def brute_force(packets: Sequence[int], children: int) -> tuple[int, tuple[int, ...]]:
    """Try every subset of ``children`` packets (exponential approach).

    The number of subsets is ``C(n, m)`` and each one costs ``O(m)`` to
    evaluate, so the complexity is ``O(C(n, m) * m)``.
    """
    _validate(packets, children)
    best_difference: int | None = None
    best_choice: tuple[int, ...] = ()
    for indices in combinations(range(len(packets)), children):
        choice = tuple(packets[index] for index in indices)
        difference = max(choice) - min(choice)
        if best_difference is None or difference < best_difference:
            best_difference = difference
            best_choice = choice
    assert best_difference is not None
    return best_difference, best_choice


def best_distribution(packets: Sequence[int], children: int) -> tuple[int, tuple[int, ...]]:
    """Efficient solution: sort, then slide a window of ``m`` packets.

    Sorting costs ``O(n log n)``.  An optimal choice can always be replaced by
    a block of ``m`` consecutive packets of the sorted list without increasing
    its spread, so one pass over the ``n - m + 1`` windows finds the answer:
    the total complexity is ``O(n log n)``.
    """
    _validate(packets, children)
    ordered = sorted(packets)
    best_difference: int | None = None
    best_choice: tuple[int, ...] = ()
    for start in range(len(ordered) - children + 1):
        window = tuple(ordered[start : start + children])
        difference = window[-1] - window[0]
        if best_difference is None or difference < best_difference:
            best_difference = difference
            best_choice = window
    assert best_difference is not None
    return best_difference, best_choice


def _validate(packets: Sequence[int], children: int) -> None:
    if children <= 0:
        raise ValueError("the number of children must be positive")
    if children > len(packets):
        raise ValueError("not enough packets for every child")
    if any(packet < 0 for packet in packets):
        raise ValueError("packet sizes must be non-negative")
