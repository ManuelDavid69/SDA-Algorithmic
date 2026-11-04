"""Tri fusion (TP 4, exercice 2)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def merge(left: list[T], right: list[T]) -> list[T]:
    """Fusionne deux listes triées en une nouvelle liste triée."""
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
    """Renvoie une nouvelle liste triée avec l'algorithme récursif de tri fusion.

    Récurrence : ``T(n) = 2 T(n/2) + Theta(n)``, d'où
    ``T(n) = Theta(n log n)`` par le théorème maître (cas 2).
    """
    if len(items) <= 1:
        return list(items)
    middle = len(items) // 2
    return merge(merge_sort(items[:middle]), merge_sort(items[middle:]))
