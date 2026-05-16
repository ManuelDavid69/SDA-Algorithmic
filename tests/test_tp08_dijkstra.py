"""Tests for TP 8: fixture, Dijkstra implementations and routing helpers."""

from __future__ import annotations

import math

import networkx as nx
import pytest

from sda.tp08_networkx.dijkstra import (
    dijkstra1,
    dijkstra2,
    dijkstra_heap,
    edge_weight,
)
from sda.tp08_networkx.fixture import (
    EDGES,
    EXPECTED_DISTANCE,
    EXPECTED_PATH,
    START,
    TARGET,
    build_graph,
    load_graph,
    write_graph,
)
from sda.tp08_networkx.routing import edge_attributes, shortest_route


def test_fixture_graph():
    graph = load_graph()
    assert graph.number_of_nodes() == 20
    assert graph.number_of_edges() == 30
    assert nx.is_connected(graph)
    assert all(1 <= data["weight"] <= 50 for _, _, data in graph.edges(data=True))
    assert len(EDGES) == 30
    assert graph[0][8]["weight"] == 36


def test_fixture_round_trip(tmp_path):
    path = tmp_path / "graph.txt"
    write_graph(path)
    graph = load_graph(path)
    assert graph.number_of_nodes() == 20
    assert graph.number_of_edges() == 30
    assert graph[13][19]["weight"] == 40


@pytest.mark.parametrize("algorithm", [dijkstra1, dijkstra2, dijkstra_heap])
def test_dijkstra_expected_route(algorithm):
    graph = load_graph()
    distance, path = algorithm(graph, START, TARGET)
    assert distance == EXPECTED_DISTANCE
    assert path == EXPECTED_PATH


@pytest.mark.parametrize("algorithm", [dijkstra1, dijkstra2, dijkstra_heap])
def test_dijkstra_matches_networkx(algorithm):
    graph = load_graph()
    for target in (1, 5, 9, 12, 17, 19):
        distance, path = algorithm(graph, 0, target)
        expected_distance = nx.shortest_path_length(graph, 0, target, weight="weight")
        expected_path = nx.shortest_path(graph, 0, target, weight="weight")
        assert distance == pytest.approx(expected_distance)
        assert sum(graph[u][v]["weight"] for u, v in zip(path, path[1:])) == pytest.approx(
            distance
        )
        # The path is a valid shortest path, even if ties could give another one.
        assert path[0] == 0 and path[-1] == target
        assert distance == pytest.approx(expected_distance)


@pytest.mark.parametrize("algorithm", [dijkstra1, dijkstra2, dijkstra_heap])
def test_dijkstra_trivial_and_unreachable(algorithm):
    graph = nx.Graph()
    graph.add_edge(1, 2, weight=5)
    graph.add_node(3)
    assert algorithm(graph, 1, 1) == (0.0, [1])
    assert algorithm(graph, 1, 3) == (math.inf, [])


@pytest.mark.parametrize("algorithm", [dijkstra1, dijkstra2, dijkstra_heap])
def test_dijkstra_unknown_node(algorithm):
    graph = load_graph()
    with pytest.raises(KeyError):
        algorithm(graph, 0, 99)


def test_dijkstra_on_directed_graph():
    graph = nx.DiGraph()
    graph.add_weighted_edges_from([(1, 2, 1), (2, 3, 1), (1, 3, 5)])
    assert dijkstra_heap(graph, 1, 3) == (2.0, [1, 2, 3])
    assert dijkstra2(graph, 3, 1) == (math.inf, [])


def test_edge_weight_forms():
    assert edge_weight({"weight": 3}) == 3
    assert edge_weight({"length": 4.5}) == 4.5
    assert edge_weight({0: {"weight": 6}}) == 6
    assert edge_weight({}) == 1
    assert edge_weight(None) == 1


def test_routing_helpers():
    graph = load_graph()
    assert edge_attributes(graph, 0, 8) == {"weight": 36.0}
    distance, path = shortest_route(graph, START, TARGET)
    assert distance == EXPECTED_DISTANCE
    assert path == EXPECTED_PATH


def test_build_graph_matches_file():
    built = build_graph()
    loaded = load_graph()
    assert set(built.edges()) == set(loaded.edges())
    for source, target in built.edges():
        assert built[source][target]["weight"] == loaded[source][target]["weight"]
