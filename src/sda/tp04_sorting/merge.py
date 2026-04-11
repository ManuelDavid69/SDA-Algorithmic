"""Merge sort (TP 4, exercise 2)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def merge(left: list[T], right: list[T]) -> list[T]:
    """Merge two sorted lists into a new sorted list."""
    result: list[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items: list[T]) -> list[T]:
    """Return a new sorted list using the recursive merge sort algorithm.

    Recurrence: ``T(n) = 2 T(n/2) + Theta(n)``, hence
    ``T(n) = Theta(n log n)`` by the Master Theorem (case 2).
    """
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    return merge(merge_sort(items[:middle]), merge_sort(items[middle:]))
