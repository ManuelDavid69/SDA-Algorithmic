"""Practical work 8: NetworkX and Dijkstra's shortest path."""

from .dijkstra import dijkstra1, dijkstra2, dijkstra_heap, edge_weight
from .fixture import (
    DATA_PATH,
    EDGES,
    EXPECTED_DISTANCE,
    EXPECTED_PATH,
    START,
    TARGET,
    build_graph,
    load_graph,
    write_graph,
)

__all__ = [
    "DATA_PATH",
    "EDGES",
    "EXPECTED_DISTANCE",
    "EXPECTED_PATH",
    "START",
    "TARGET",
    "build_graph",
    "dijkstra1",
    "dijkstra2",
    "dijkstra_heap",
    "edge_weight",
    "load_graph",
    "write_graph",
]
