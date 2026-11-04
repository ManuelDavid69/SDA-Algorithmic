"""Assistants OSMnx pour le calculateur d'itinéraire (TP 8, exercice 3).

La dépendance est facultative : installez-la avec ``pip install -e .[routing]``.
Les fonctions sont importées paresseusement afin que le reste du dépôt
fonctionne sans OSMnx ni GeoPandas.
"""

from __future__ import annotations

from typing import Any

import networkx as nx

from .dijkstra import dijkstra_heap


def _require_osmnx():
    try:
        import osmnx as ox
    except ImportError as error:  # pragma: no cover - dépend de l'environnement
        raise ImportError(
            "OSMnx n'est pas installé ; exécutez `pip install -e .[routing]` "
            "ou `pip install osmnx geopandas`."
        ) from error
    return ox


def load_city_graph(place: str = "Lyon, France", network_type: str = "drive") -> nx.MultiDiGraph:
    """Télécharge le réseau routier de ``place`` depuis OpenStreetMap."""
    ox = _require_osmnx()
    return ox.graph_from_place(place, network_type=network_type)


def nearest_node(graph: nx.Graph, latitude: float, longitude: float) -> int:
    """Renvoie le nœud du graphe le plus proche d'un point géographique."""
    ox = _require_osmnx()
    return ox.distance.nearest_nodes(graph, X=longitude, Y=latitude)


def edge_attributes(graph: nx.Graph, source: int, target: int) -> Any:
    """Attributs d'une arête, tels que renvoyés par ``get_edge_data``.

    OSMnx utilise un MultiDiGraph, le résultat est donc généralement
    ``{0: {"length": ..., "highway": ...}}``.
    """
    return graph.get_edge_data(source, target)


def shortest_route(
    graph: nx.Graph, start: int, target: int
) -> tuple[float, list[int]]:
    """Plus court chemin avec la version à tas de Dijkstra.

    ``edge_weight`` comprend à la fois l'attribut ``length`` d'OSMnx et le
    dictionnaire imbriqué d'un MultiDiGraph.
    """
    return dijkstra_heap(graph, start, target)


def plot_route(graph: nx.Graph, route: list[int], **kwargs):
    """Dessine le graphe et l'itinéraire sur une figure Matplotlib."""
    ox = _require_osmnx()
    return ox.plot_graph_route(graph, route, **kwargs)
