"""Recherche séquentielle et dichotomique (TP 3, exercice 5)."""

from __future__ import annotations

from collections.abc import Sequence


def linear_search(items: Sequence[int], target: int) -> int:
    """Renvoie l'indice de ``target``, ou ``-1``.

    Pire cas ``O(n)``, meilleur cas ``O(1)`` ; le cas moyen est ``O(n)``.
    """
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def binary_search_recursive(items: Sequence[int], target: int) -> int:
    """Recherche dichotomique récursive sur une liste triée par ordre croissant.

    La récurrence est ``T(n) = T(n/2) + O(1)``, d'où ``O(log n)``.
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
    """Version itérative du même algorithme."""
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


# Nom utilisé dans l'énoncé.
dicho = binary_search_recursive
