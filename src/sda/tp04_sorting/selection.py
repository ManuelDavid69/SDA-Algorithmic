"""Selection sort (TP 4, exercise 1)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def selection_sort(items: list[T]) -> list[T]:
    """Sort ``items`` in place with the selection sort algorithm.

    Loop invariant: before iteration ``i``, ``items[:i]`` contains the ``i``
    smallest elements of the list, in sorted order.  At iteration ``i`` the
    algorithm selects the smallest element of ``items[i:]`` and swaps it into
    position ``i``.

    The number of comparisons is ``n(n-1)/2`` in every case, so the time
    complexity is ``Theta(n^2)`` in the best and in the worst case.
    """
    for i in range(len(items)):
        minimum = i
        for j in range(i + 1, len(items)):
            if items[j] < items[minimum]:
                minimum = j
        if minimum != i:
            items[i], items[minimum] = items[minimum], items[i]
    return items
