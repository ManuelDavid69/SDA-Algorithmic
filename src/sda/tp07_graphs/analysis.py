"""Written answers to the graph TD, computed on the graphs of the statement."""

from __future__ import annotations

from .examples import (
    course_graph,
    envelope_graph,
    language_bipartite_graph,
    petersen_graph,
    shared_course_pairs,
    students_graph,
)


def petersen_report() -> dict:
    graph = petersen_graph()
    induced_vertices = [6, 3, 7, 8, 1, 5]
    induced = graph.subgraph(induced_vertices)
    return {
        "directed": graph.directed,
        "vertices": sorted(graph.vertices),
        "edges": sorted(graph.edges()),
        "neighbours_of_2": sorted(graph.neighbours(2)),
        "degree_of_10": graph.degree(10),
        "regular": graph.is_regular(),
        "regularity": graph.regularity(),
        "connected": graph.is_connected(),
        "bipartite": graph.is_bipartite()[0],
        "planar": False,
        "adjacency_matrix": graph.adjacency_matrix(sorted(graph.vertices)),
        "incidence_matrix": graph.incidence_matrix(
            sorted(graph.vertices), sorted(graph.edges())
        ),
        "induced_vertices": induced_vertices,
        "induced_edges": sorted(induced.edges()),
        "chromatic_number": graph.chromatic_number(),
        "independence_number": len(graph.max_independent_set()),
        "maximum_matching": len(graph.max_matching()),
        "minimum_vertex_cover": len(graph.min_vertex_cover()),
    }


def scheduling_report() -> dict:
    students = students_graph()
    courses = course_graph()
    return {
        "pairs": shared_course_pairs(),
        "number_of_pairs": len(shared_course_pairs()),
        "max_group_without_common_course": students.max_independent_set(),
        "message_diffusion_possible": language_bipartite_graph().is_connected(),
        "max_courses_per_slot": courses.chromatic_number(),
        "number_of_slots": courses.chromatic_number(),
        "course_coloring": courses.greedy_coloring(),
        "course_edges": sorted(courses.edges()),
    }


def envelope_report() -> dict:
    graph = envelope_graph()
    odd = sorted(vertex for vertex in graph.vertices if graph.degree(vertex) % 2)
    circuit = graph.eulerian_circuit()
    path = graph.eulerian_path()
    return {
        "degrees": {vertex: graph.degree(vertex) for vertex in sorted(graph.vertices)},
        "odd_vertices": odd,
        "eulerian_circuit": circuit,
        "eulerian_path": path,
        "start": path[0] if path else None,
        "end": path[-1] if path else None,
    }


def ambassadors_possible(people: int, acquaintances: int) -> bool:
    """Handshake lemma: the sum of the degrees must be even."""
    return (people * acquaintances) % 2 == 0


def ambassadors_report() -> dict:
    return {
        "48_people": ambassadors_possible(48, 11),
        "47_people": ambassadors_possible(47, 11),
        "49_people": ambassadors_possible(49, 11),
        "handshakes_48": 48 * 47 // 2,
    }
