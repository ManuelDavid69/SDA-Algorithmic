"""Démonstration du TP 7 : graphe de Petersen, ordonnancement, Euler et couvertures."""

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
    print("== Graphe de Petersen ==")
    print(f"{graph}")
    print(f"voisins de 2 : {sorted(graph.neighbours(2))}")
    print(f"degré de 10 : {graph.degree(10)}")
    print(f"régulier : {graph.is_regular()} (degré {graph.regularity()})")
    print(f"connexe : {graph.is_connected()}, biparti : {graph.is_bipartite()[0]}")
    print("matrice d'adjacence :")
    for row in graph.adjacency_matrix(sorted(graph.vertices)):
        print("  " + " ".join(map(str, row)))
    report = petersen_report()
    print(f"nombre chromatique : {report['chromatic_number']}")
    print(f"nombre d'indépendance : {report['independence_number']}")
    print(f"couplage maximum : {report['maximum_matching']}")
    print(f"couverture de sommets minimale : {report['minimum_vertex_cover']}")
    print(f"arêtes induites sur {{1,3,5,6,7,8}} : {report['induced_edges']}")

    print("\n== Emploi du temps des langues ==")
    scheduling = scheduling_report()
    print(f"paires partageant un cours : {scheduling['pairs']}")
    print(f"plus grand groupe sans cours commun : {scheduling['max_group_without_common_course']}")
    print(f"diffusion du message possible : {scheduling['message_diffusion_possible']}")
    print(f"cours par créneau : {scheduling['max_courses_per_slot']}")
    print(f"nombre de créneaux : {scheduling['number_of_slots']}")
    print(f"une coloration : {scheduling['course_coloring']}")

    print("\n== Enveloppe ==")
    report = envelope_report()
    print(f"degrés : {report['degrees']}")
    print(f"sommets de degré impair : {report['odd_vertices']}")
    print(f"circuit eulérien : {report['eulerian_circuit']}")
    print(f"chaîne eulérienne : {' -> '.join(report['eulerian_path'])}")
    print(f"début : {report['start']}, fin : {report['end']}")

    print("\n== Ambassadeurs ==")
    for key, value in ambassadors_report().items():
        print(f"{key}: {value}")

    print("\n== Couverture d'arêtes d'un petit graphe ==")
    small = envelope_graph()
    cover = small.min_edge_cover()
    print(f"couverture d'arêtes minimale : {cover}")
    print(f"couverture de sommets minimale : {small.min_vertex_cover()}")


if __name__ == "__main__":
    main()
