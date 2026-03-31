"""Sequential and dichotomic search (TP 3, exercise 5)."""

from __future__ import annotations

from typing import Sequence


def linear_search(items: Sequence[int], target: int) -> int:
    """Return the index of ``target``, or ``-1``.

    Worst case ``O(n)``, best case ``O(1)``; the average case is ``O(n)``.
    """
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def binary_search_recursive(items: Sequence[int], target: int) -> int:
    """Recursive binary search on a list sorted in increasing order.

    The recurrence is ``T(n) = T(n/2) + O(1)``, hence ``O(log n)``.
    """
    return _binary_search(items, target, 0, len(items) - 1)


def _binary_search(items: Sequence[int], target: int, low: int, high: int) -> int:
    if low > high:
        return -1
    middle = (low + high) // 2
    if items[middle] == target:
        return middle
    if items[middle] > target:
        return _binary_search(items, target, low, middle - 1)
    return _binary_search(items, target, middle + 1, high)


def binary_search_iterative(items: Sequence[int], target: int) -> int:
    """Iterative version of the same algorithm."""
    low, high = 0, len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] > target:
            high = middle - 1
        else:
            low = middle + 1
    return -1


# Name used in the statement.
dicho = binary_search_recursive
