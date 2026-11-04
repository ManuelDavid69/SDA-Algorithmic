"""Démonstration du TP 4 : algorithmes de tri et distribution de bonbons."""

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
    print(f"entrée           : {values}")
    print(f"tri par sélection: {selection_sort(list(values))}")
    print(f"tri fusion       : {merge_sort(values)}")
    print(f"tri aux deux tiers: {thirds_sort(list(values))}")

    print("\n== Temps d'exécution sur 400 éléments ==")
    large = [random.randint(0, 1000) for _ in range(400)]
    for name, algorithm in (
        ("sélection", selection_sort),
        ("fusion", merge_sort),
        ("deux tiers", thirds_sort),
    ):
        start = time.perf_counter()
        algorithm(list(large))
        elapsed = time.perf_counter() - start
        print(f"{name:>11}: {elapsed * 1e3:8.2f} ms")

    print("\n== Distribution de bonbons ==")
    packets = [7, 3, 2, 9, 12, 5, 8, 4]
    children = 3
    print(f"paquets : {packets}, enfants : {children}")
    difference, choice = brute_force(packets, children)
    print(f"force brute : différence {difference}, choix {choice}")
    difference, choice = best_distribution(packets, children)
    print(f"fenêtre glissante : différence {difference}, choix {choice}")


if __name__ == "__main__":
    main()
