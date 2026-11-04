"""Démonstration du TP 8 : NetworkX, Dijkstra et comparaison d'itinéraires."""

from __future__ import annotations

import time

import networkx as nx

from .dijkstra import dijkstra1, dijkstra2, dijkstra_heap
from .fixture import EXPECTED_DISTANCE, EXPECTED_PATH, START, TARGET, load_graph


def _timed(algorithm, graph, start, target):
    begin = time.perf_counter()
    result = algorithm(graph, start, target)
    return result, time.perf_counter() - begin


def main() -> None:
    graph = load_graph()
    print("== Graphe de référence ==")
    print(f"sommets : {graph.number_of_nodes()}, arêtes : {graph.number_of_edges()}")
    print(f"connexe : {nx.is_connected(graph)}")
    print(f"itinéraire attendu : {EXPECTED_PATH} (longueur {EXPECTED_DISTANCE})")

    for algorithm in (dijkstra1, dijkstra2, dijkstra_heap):
        (distance, path), elapsed = _timed(algorithm, graph, START, TARGET)
        print(
            f"{algorithm.__name__:>13}: longueur {distance:>6}, "
            f"chemin {path}, {elapsed * 1e6:8.1f} us"
        )

    print("\n== Comparaison sur un graphe plus grand ==")
    seed = 0
    while True:
        large = nx.gnm_random_graph(400, 900, seed=seed)
        if nx.is_connected(large):
            break
        seed += 1
    for source, target in large.edges():
        large[source][target]["weight"] = (source * 31 + target * 17) % 50 + 1
    print(f"graine {seed} : {large.number_of_nodes()} sommets, {large.number_of_edges()} arêtes")
    reference = nx.shortest_path_length(large, 0, 399, weight="weight")
    for algorithm in (dijkstra1, dijkstra2, dijkstra_heap):
        (distance, path), elapsed = _timed(algorithm, large, 0, 399)
        assert distance == reference
        print(f"{algorithm.__name__:>13}: longueur {distance:>8}, {elapsed * 1e3:8.2f} ms")


if __name__ == "__main__":
    main()
