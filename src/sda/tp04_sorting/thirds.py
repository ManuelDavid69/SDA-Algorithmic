"""Tri aux deux tiers (TP 4, exercice 3, annales 2024)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def thirds_sort(items: list[T]) -> list[T]:
    """Trie ``items`` sur place avec l'algorithme récursif aux deux tiers.

    L'algorithme trie les deux premiers tiers, puis les deux derniers tiers,
    puis à nouveau les deux premiers tiers.  Sa récurrence est
    ``T(n) = 3 T(2n/3) + Theta(1)``, d'où
    ``T(n) = Theta(n^(log_(3/2)(3))) = Theta(n^2.71)``.
    """
    _sort_range(items, 0, len(items))
    return items


def _sort_range(items: list[T], low: int, high: int) -> None:
    size = high - low
    if size <= 2:
        if size == 2 and items[low + 1] < items[low]:
            items[low], items[low + 1] = items[low + 1], items[low]
        return
    two_thirds = (2 * size + 2) // 3  # plafond(2 * size / 3)
    _sort_range(items, low, low + two_thirds)
    _sort_range(items, high - two_thirds, high)
    _sort_range(items, low, low + two_thirds)
