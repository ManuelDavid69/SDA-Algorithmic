"""Demonstration of TP 7: Petersen graph, scheduling, Euler and covers."""

from __future__ import annotations

from .analysis import (
    ambassadors_report,
    envelope_report,
    petersen_report,
    scheduling_report,
)
from .examples import envelope_graph, petersen_graph


def main() -> None:
    graph = petersen_graph()
    print("== Petersen graph ==")
    print(f"{graph}")
    print(f"neighbours of 2: {sorted(graph.neighbours(2))}")
    print(f"degree of 10: {graph.degree(10)}")
    print(f"regular: {graph.is_regular()} (degree {graph.regularity()})")
    print(f"connected: {graph.is_connected()}, bipartite: {graph.is_bipartite()[0]}")
    print("adjacency matrix:")
    for row in graph.adjacency_matrix(sorted(graph.vertices)):
        print("  " + " ".join(map(str, row)))
    report = petersen_report()
    print(f"chromatic number: {report['chromatic_number']}")
    print(f"independence number: {report['independence_number']}")
    print(f"maximum matching: {report['maximum_matching']}")
    print(f"minimum vertex cover: {report['minimum_vertex_cover']}")
    print(f"induced edges on {{1,3,5,6,7,8}}: {report['induced_edges']}")

    print("\n== Language timetable ==")
    scheduling = scheduling_report()
    print(f"pairs sharing a course: {scheduling['pairs']}")
    print(f"largest group without a common course: {scheduling['max_group_without_common_course']}")
    print(f"message diffusion possible: {scheduling['message_diffusion_possible']}")
    print(f"courses per slot: {scheduling['max_courses_per_slot']}")
    print(f"number of slots: {scheduling['number_of_slots']}")
    print(f"one colouring: {scheduling['course_coloring']}")

    print("\n== Envelope ==")
    report = envelope_report()
    print(f"degrees: {report['degrees']}")
    print(f"odd vertices: {report['odd_vertices']}")
    print(f"Eulerian circuit: {report['eulerian_circuit']}")
    print(f"Eulerian path: {' -> '.join(report['eulerian_path'])}")
    print(f"start: {report['start']}, end: {report['end']}")

    print("\n== Ambassadors ==")
    for key, value in ambassadors_report().items():
        print(f"{key}: {value}")

    print("\n== Edge cover of a small graph ==")
    small = envelope_graph()
    cover = small.min_edge_cover()
    print(f"minimum edge cover: {cover}")
    print(f"minimum vertex cover: {small.min_vertex_cover()}")


if __name__ == "__main__":
    main()
