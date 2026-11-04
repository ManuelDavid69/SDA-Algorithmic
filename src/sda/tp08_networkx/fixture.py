"""Graphe pondéré déterministe utilisé par les TP sur Dijkstra (TP 8).

Le sujet fournit un graphe aléatoire à 20 sommets et 30 arêtes. Nous utilisons
une liste d'arêtes fixe afin que les tests et le carnet soient reproductibles ;
le format est la même liste d'adjacence multiligne que dans l'énoncé.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx

DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "tp08_graph.txt"

# (source, cible, poids)
EDGES: list[tuple[int, int, int]] = [
    (0, 8, 36),
    (0, 9, 50),
    (0, 12, 29),
    (1, 2, 33),
    (1, 7, 30),
    (1, 8, 29),
    (2, 17, 13),
    (2, 19, 38),
    (3, 5, 33),
    (3, 12, 12),
    (4, 15, 31),
    (5, 7, 40),
    (5, 9, 41),
    (5, 14, 12),
    (6, 8, 7),
    (6, 13, 29),
    (7, 9, 20),
    (7, 16, 10),
    (8, 11, 6),
    (8, 14, 45),
    (8, 15, 35),
    (9, 11, 3),
    (9, 13, 29),
    (9, 16, 26),
    (9, 17, 41),
    (9, 18, 39),
    (10, 12, 42),
    (10, 15, 48),
    (13, 19, 40),
    (16, 17, 42),
]

START = 0
TARGET = 19
EXPECTED_PATH = [0, 8, 6, 13, 19]
EXPECTED_DISTANCE = 112


def build_graph() -> nx.Graph:
    graph = nx.Graph()
    graph.add_weighted_edges_from(EDGES)
    return graph


def write_graph(path: str | Path = DATA_PATH) -> None:
    """Écrit le graphe au format de liste d'adjacence multiligne de NetworkX.

    L'en-tête est fixe (sans horodatage) afin que le fichier de référence
    versionné soit reproductible octet pour octet.
    """
    graph = build_graph()
    lines = ["# Graphe pondéré du TP 8 : 20 sommets, 30 arêtes"]
    for node in sorted(graph.nodes):
        neighbours = sorted(graph[node])
        lines.append(f"{node} {len(neighbours)}")
        for neighbour in neighbours:
            weight = graph[node][neighbour]["weight"]
            lines.append(f"{neighbour} {{'weight': {weight}}}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_graph(path: str | Path = DATA_PATH) -> nx.Graph:
    """Lit le graphe et normalise les poids en valeurs ``float``."""
    graph = nx.read_multiline_adjlist(path, nodetype=int)
    for source, target, data in graph.edges(data=True):
        if "weight" in data:
            graph[source][target]["weight"] = float(data["weight"])
    return graph
