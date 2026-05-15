"""Dijkstra's shortest path algorithm, with three visited-set strategies."""

from __future__ import annotations

import heapq
import math
from typing import Any

import networkx as nx


def edge_weight(data: Any) -> float:
    """Extract the weight of an edge from a NetworkX data dictionary.

    Handles the simple ``{"weight": w}`` form, the ``{"length": w}`` form used
    by OSMnx, and the nested ``{0: {"weight": w}}`` form of a MultiDiGraph.
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
            raise KeyError(f"node {node!r} is not in the graph")


def _reconstruct(previous: dict, start: int, target: int) -> list[int]:
    path = [target]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return path


def dijkstra1(graph: nx.Graph, start: int, target: int) -> tuple[float, list[int]]:
    """Reference version: the visited vertices are kept in a **list**.

    ``vertex in visited`` is ``O(V)``, hence the loop wastes ``O(V^2)`` on
    membership tests in addition to the ``O(V^2)`` minimum search.  This is the
    version asked for in question 2 of the statement.
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
    """Same algorithm, but the visited vertices are stored in a **set**.

    Membership becomes ``O(1)``, so the only remaining quadratic part is the
    linear search for the minimum.  The result is identical to `dijkstra1`.
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
    """Dijkstra with a binary heap: ``O((V + E) log V)``.

    NetworkX does not support decrease-key on an arbitrary heap, so a stale
    ``(distance, node)`` pair is simply skipped when it is popped.
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
