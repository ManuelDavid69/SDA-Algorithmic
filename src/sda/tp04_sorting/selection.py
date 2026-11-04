"""Tri par sélection (TP 4, exercice 1)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def selection_sort(items: list[T]) -> list[T]:
    """Trie ``items`` sur place avec l'algorithme de tri par sélection.

    Invariant de boucle : avant l'itération ``i``, ``items[:i]`` contient les
    ``i`` plus petits éléments de la liste, dans l'ordre trié.  À l'itération
    ``i``, l'algorithme sélectionne le plus petit élément de ``items[i:]`` et
    l'échange avec la position ``i``.

    Le nombre de comparaisons est ``n(n-1)/2`` dans tous les cas, la
    complexité en temps est donc ``Theta(n^2)`` au meilleur comme au pire cas.
    """
    for i in range(len(items)):
        minimum = i
        for j in range(i + 1, len(items)):
            if items[j] < items[minimum]:
                minimum = j
        if minimum != i:
            items[i], items[minimum] = items[minimum], items[i]
    return items
