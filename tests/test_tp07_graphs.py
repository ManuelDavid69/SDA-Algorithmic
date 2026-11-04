"""Tests du TP 7 : représentation des graphes, parcours et algorithmes de graphes."""

import pytest

from sda.tp07_graphs.analysis import (
    ambassadors_possible,
    ambassadors_report,
    envelope_report,
    petersen_report,
    scheduling_report,
)
from sda.tp07_graphs.examples import (
    course_graph,
    envelope_graph,
    language_bipartite_graph,
    petersen_graph,
    shared_course_pairs,
    students_graph,
)
from sda.tp07_graphs.graph import Graph


def triangle() -> Graph:
    return Graph.from_edges([(1, 2), (2, 3), (3, 1)])


def path3() -> Graph:
    return Graph.from_edges([(1, 2), (2, 3)])


def cycle4() -> Graph:
    return Graph.from_edges([(1, 2), (2, 3), (3, 4), (4, 1)])


def star() -> Graph:
    return Graph.from_edges([("c", "a"), ("c", "b"), ("c", "d")])


def test_graph_basics():
    graph = triangle()
    assert graph.order == 3
    assert graph.size == 3
    assert sorted(graph.vertices) == [1, 2, 3]
    assert {frozenset(edge) for edge in graph.edges()} == {
        frozenset((1, 2)),
        frozenset((2, 3)),
        frozenset((3, 1)),
    }
    assert graph.degree(1) == 2
    assert graph.is_regular()
    assert graph.regularity() == 2
    assert graph.is_connected()
    assert not graph.is_bipartite()[0]
    assert graph.has_cycle()
    assert repr(graph) == "Graph(undirected, vertices=3, edges=3)"


def test_adjacency_and_incidence_matrices():
    graph = triangle()
    assert graph.adjacency_matrix([1, 2, 3]) == [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
    incidence = graph.incidence_matrix([1, 2, 3], [(1, 2), (2, 3), (3, 1)])
    assert all(sum(row) == 2 for row in incidence)


def test_directed_graph():
    graph = Graph(directed=True)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    assert graph.size == 2
    assert graph.neighbours(1) == [2]
    assert graph.out_degree(1) == 1
    assert graph.in_degree(1) == 0
    assert graph.degree(2) == 2
    assert graph.eulerian_path() == [1, 2, 3]
    assert graph.eulerian_circuit() is None


def test_subgraph_and_complement():
    graph = triangle()
    subgraph = graph.subgraph([1, 2])
    assert sorted(subgraph.edges()) == [(1, 2)]
    complement = graph.complement()
    assert complement.order == 3
    assert complement.size == 0
    assert sorted(complement.edges()) == []


def test_bfs_dfs_and_components():
    graph = Graph.from_edges([(1, 2), (2, 3), (4, 5)])
    assert graph.bfs(1) == [1, 2, 3]
    assert graph.dfs(1) == [1, 2, 3]
    assert graph.is_connected() is False
    components = sorted(sorted(component) for component in graph.connected_components())
    assert components == [[1, 2, 3], [4, 5]]
    assert graph.distances(1) == {1: 0, 2: 1, 3: 2}
    with pytest.raises(KeyError):
        graph.bfs(99)


def test_bipartite_and_cycle():
    assert path3().is_bipartite()[0]
    assert cycle4().is_bipartite()[0]
    assert not triangle().is_bipartite()[0]
    assert not path3().has_cycle()
    assert cycle4().has_cycle()
    assert not star().has_cycle()


def test_eulerian_paths():
    assert cycle4().eulerian_circuit() is not None
    assert path3().eulerian_circuit() is None
    assert path3().eulerian_path() == [1, 2, 3]
    assert path3().eulerian_path()[0] in (1, 3)
    assert star().eulerian_circuit() is None
    # Une étoile à quatre feuilles a quatre sommets impairs : pas de chemin eulérien.
    assert star().eulerian_path() is None


def test_colouring_and_covers():
    assert triangle().chromatic_number() == 3
    assert path3().chromatic_number() == 2
    assert cycle4().chromatic_number() == 2
    assert Graph().chromatic_number() == 0

    assert len(triangle().max_independent_set()) == 1
    assert len(path3().max_independent_set()) == 2
    assert len(star().max_independent_set()) == 3

    assert len(triangle().max_matching()) == 1
    assert len(cycle4().max_matching()) == 2
    assert len(star().max_matching()) == 1

    assert len(triangle().min_vertex_cover()) == 2
    assert len(path3().min_vertex_cover()) == 1
    assert len(star().min_vertex_cover()) == 1

    assert len(triangle().min_edge_cover()) == 2
    assert len(path3().min_edge_cover()) == 2
    assert len(star().min_edge_cover()) == 3
    assert Graph.from_edges([(1, 2)]).subgraph([1]).min_edge_cover() is None


def test_greedy_colouring_is_valid():
    graph = petersen_graph()
    colors = graph.greedy_coloring()
    assert set(colors.values()) == {0, 1, 2}
    for source, target in graph.edges():
        assert colors[source] != colors[target]


def test_isomorphism():
    assert triangle().is_isomorphic(Graph.from_edges([("a", "b"), ("b", "c"), ("c", "a")]))
    assert not triangle().is_isomorphic(path3())
    assert cycle4().is_isomorphic(Graph.from_edges([(10, 20), (20, 30), (30, 40), (40, 10)]))
    assert not cycle4().is_isomorphic(path3())
    assert petersen_graph().is_isomorphic(
        Graph.from_edges([(i + 100, j + 100) for i, j in petersen_graph().edges()])
    )


def test_petersen_graph():
    graph = petersen_graph()
    assert graph.order == 10
    assert graph.size == 15
    assert graph.regularity() == 3
    assert graph.neighbours(2) == [7, 4, 5] or set(graph.neighbours(2)) == {4, 5, 7}
    assert graph.degree(10) == 3
    assert graph.is_connected()
    assert not graph.is_bipartite()[0]
    assert graph.chromatic_number() == 3
    assert len(graph.max_independent_set()) == 4
    assert len(graph.max_matching()) == 5
    assert len(graph.min_vertex_cover()) == 6


def test_petersen_report():
    report = petersen_report()
    assert report["directed"] is False
    assert report["neighbours_of_2"] == [4, 5, 7]
    assert report["degree_of_10"] == 3
    assert report["regular"] is True
    assert report["connected"] is True
    assert report["planar"] is False
    assert report["induced_edges"] == [
        (1, 3),
        (3, 5),
        (6, 1),
        (6, 7),
        (7, 8),
        (8, 3),
    ]
    assert report["chromatic_number"] == 3
    assert report["independence_number"] == 4
    assert report["maximum_matching"] == 5
    assert report["minimum_vertex_cover"] == 6
    assert len(report["adjacency_matrix"]) == 10
    assert len(report["incidence_matrix"]) == 10


def test_language_graphs_and_scheduling():
    students = students_graph()
    courses = course_graph()
    bipartite = language_bipartite_graph()
    assert bipartite.is_bipartite()[0]
    assert bipartite.is_connected()
    assert len(shared_course_pairs()) == 7
    assert ("Axel", "Corentin") in shared_course_pairs()
    assert len(students.max_independent_set()) == 2
    assert courses.chromatic_number() == 3

    report = scheduling_report()
    assert report["number_of_pairs"] == 7
    assert len(report["max_group_without_common_course"]) == 2
    assert report["message_diffusion_possible"] is True
    assert report["max_courses_per_slot"] == 3
    assert report["number_of_slots"] == 3


def test_envelope():
    graph = envelope_graph()
    assert graph.size == 8
    report = envelope_report()
    assert report["odd_vertices"] == ["LL", "LR"]
    assert report["eulerian_circuit"] is None
    assert report["eulerian_path"] is not None
    assert len(report["eulerian_path"]) == 9
    assert {report["start"], report["end"]} == {"LL", "LR"}


def test_ambassadors():
    assert ambassadors_possible(48, 11) is True
    assert ambassadors_possible(47, 11) is False
    assert ambassadors_possible(49, 11) is False
    assert ambassadors_report()["handshakes_48"] == 1128
