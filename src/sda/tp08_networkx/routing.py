"""OSMnx helpers for the route calculator (TP 8, exercise 3).

The dependency is optional: install it with ``pip install -e .[routing]``.
The functions are imported lazily so that the rest of the repository works
without OSMnx and GeoPandas.
"""

from __future__ import annotations

from typing import Any

import networkx as nx

from .dijkstra import dijkstra_heap


def _require_osmnx():
    try:
        import osmnx as ox
    except ImportError as error:  # pragma: no cover - depends on the environment
        raise ImportError(
            "OSMnx is not installed; run `pip install -e .[routing]` "
            "or `pip install osmnx geopandas`."
        ) from error
    return ox


def load_city_graph(place: str = "Lyon, France", network_type: str = "drive") -> nx.MultiDiGraph:
    """Download the street network of ``place`` from OpenStreetMap."""
    ox = _require_osmnx()
    return ox.graph_from_place(place, network_type=network_type)


def nearest_node(graph: nx.Graph, latitude: float, longitude: float) -> int:
    """Return the graph node closest to a geographic point."""
    ox = _require_osmnx()
    return ox.distance.nearest_nodes(graph, X=longitude, Y=latitude)


def edge_attributes(graph: nx.Graph, source: int, target: int) -> Any:
    """Attributes of an edge, as returned by ``get_edge_data``.

    OSMnx uses a MultiDiGraph, so the result is usually
    ``{0: {"length": ..., "highway": ...}}``.
    """
    return graph.get_edge_data(source, target)


def shortest_route(
    graph: nx.Graph, start: int, target: int
) -> tuple[float, list[int]]:
    """Shortest route with the heap version of Dijkstra.

    ``edge_weight`` understands both the ``length`` attribute of OSMnx and the
    nested dictionary of a MultiDiGraph.
    """
    return dijkstra_heap(graph, start, target)


def plot_route(graph: nx.Graph, route: list[int], **kwargs):
    """Draw the graph and the route on a Matplotlib figure."""
    ox = _require_osmnx()
    return ox.plot_graph_route(graph, route, **kwargs)
