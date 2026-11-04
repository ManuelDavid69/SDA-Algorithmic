"""Algorithme de plus court chemin de Dijkstra, avec trois stratégies d'ensemble des visités."""

from __future__ import annotations

import heapq
import math
from typing import Any

import networkx as nx


def edge_weight(data: Any) -> float:
    """Extrait le poids d'une arête d'un dictionnaire de données NetworkX.

    Gère la forme simple ``{"weight": w}``, la forme ``{"length": w}`` utilisée
    par OSMnx, et la forme imbriquée ``{0: {"weight": w}}`` d'un MultiDiGraph.
    """
    if isinstance(data, dict):
        if "weight" in data:
            return float(data["weight"])
        if "length" in data:
            return float(data["length"])
        if 0 in data and isinstance(data[0], dict):
            return edge_weight(data[0])
    return 1.0


def _check_nodes(graph: nx.Graph, *nodes: int) -> None:
    for node in nodes:
        if node not in graph:
            raise KeyError(f"le nœud {node!r} n'est pas dans le graphe")


def _reconstruct(previous: dict, start: int, target: int) -> list[int]:
    path = [target]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def dijkstra1(graph: nx.Graph, start: int, target: int) -> tuple[float, list[int]]:
    """Version de référence : les sommets visités sont conservés dans une **liste**.

    ``vertex in visited`` est en ``O(V)``, donc la boucle gaspille ``O(V^2)`` en
    tests d'appartenance en plus de la recherche du minimum en ``O(V^2)``.
    C'est la version demandée à la question 2 de l'énoncé.
    """
    _check_nodes(graph, start, target)
    distances: dict[int, float] = {start: 0.0}
    previous: dict[int, int] = {}
    visited: list[int] = []

    while True:
        candidates = [node for node in distances if node not in visited]
        if not candidates:
            break
        current = min(candidates, key=lambda node: distances[node])
        if current == target:
            break
        visited.append(current)
        for neighbour, data in graph[current].items():
            if neighbour in visited:
                continue
            candidate = distances[current] + edge_weight(data)
            if candidate < distances.get(neighbour, math.inf):
                distances[neighbour] = candidate
                previous[neighbour] = current

    if target not in distances:
        return math.inf, []
    return distances[target], _reconstruct(previous, start, target)


def dijkstra2(graph: nx.Graph, start: int, target: int) -> tuple[float, list[int]]:
    """Même algorithme, mais les sommets visités sont stockés dans un **ensemble**.

    L'appartenance devient ``O(1)``, la seule partie quadratique restante est
    donc la recherche linéaire du minimum. Le résultat est identique à
    `dijkstra1`.
    """
    _check_nodes(graph, start, target)
    distances: dict[int, float] = {start: 0.0}
    previous: dict[int, int] = {}
    visited: set[int] = set()

    while True:
        candidates = [node for node in distances if node not in visited]
        if not candidates:
            break
        current = min(candidates, key=lambda node: distances[node])
        if current == target:
            break
        visited.add(current)
        for neighbour, data in graph[current].items():
            if neighbour in visited:
                continue
            candidate = distances[current] + edge_weight(data)
            if candidate < distances.get(neighbour, math.inf):
                distances[neighbour] = candidate
                previous[neighbour] = current

    if target not in distances:
        return math.inf, []
    return distances[target], _reconstruct(previous, start, target)


def dijkstra_heap(graph: nx.Graph, start: int, target: int) -> tuple[float, list[int]]:
    """Dijkstra avec un tas binaire : ``O((V + E) log V)``.

    NetworkX ne prend pas en charge la diminution de clé sur un tas quelconque,
    une paire ``(distance, node)`` obsolète est donc simplement ignorée
    lorsqu'elle est extraite.
    """
    _check_nodes(graph, start, target)
    distances: dict[int, float] = {start: 0.0}
    previous: dict[int, int] = {}
    queue: list[tuple[float, int]] = [(0.0, start)]
    visited: set[int] = set()

    while queue:
        distance, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        if current == target:
            break
        for neighbour, data in graph[current].items():
            if neighbour in visited:
                continue
            candidate = distance + edge_weight(data)
            if candidate < distances.get(neighbour, math.inf):
                distances[neighbour] = candidate
                previous[neighbour] = current
                heapq.heappush(queue, (candidate, neighbour))

    if target not in distances:
        return math.inf, []
    return distances[target], _reconstruct(previous, start, target)
