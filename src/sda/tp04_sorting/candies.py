"""Problème de distribution de bonbons (TP 4, exercice 4).

Étant donné ``n`` paquets de bonbons et ``m`` enfants, choisir exactement ``m``
paquets de sorte que la différence entre le plus grand et le plus petit paquet
choisi soit minimale.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import combinations


def brute_force(packets: Sequence[int], children: int) -> tuple[int, tuple[int, ...]]:
    """Essaie tous les sous-ensembles de ``children`` paquets (approche exponentielle).

    Le nombre de sous-ensembles est ``C(n, m)`` et chacun coûte ``O(m)`` à
    évaluer, la complexité est donc ``O(C(n, m) * m)``.
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
    """Solution efficace : trier, puis faire glisser une fenêtre de ``m`` paquets.

    Le tri coûte ``O(n log n)``.  Un choix optimal peut toujours être remplacé
    par un bloc de ``m`` paquets consécutifs de la liste triée sans augmenter
    son étendue ; un seul parcours des ``n - m + 1`` fenêtres fournit donc la
    réponse : la complexité totale est ``O(n log n)``.
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
        raise ValueError("le nombre d'enfants doit être strictement positif")
    if children > len(packets):
        raise ValueError("pas assez de paquets pour chaque enfant")
    if any(packet < 0 for packet in packets):
        raise ValueError("les tailles de paquets doivent être positives ou nulles")
