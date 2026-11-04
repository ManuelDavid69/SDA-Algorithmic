"""Graphes utilisés en TD et TP 7."""

from __future__ import annotations

from itertools import combinations

from .graph import Graph

PETERSEN_EDGES = [
    # pentagone extérieur
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 6),
    # rayons
    (6, 1),
    (7, 2),
    (8, 3),
    (9, 4),
    (10, 5),
    # pentagramme intérieur
    (1, 3),
    (3, 5),
    (5, 2),
    (2, 4),
    (4, 1),
]

ENVELOPE_EDGES = [
    ("T", "UL"),
    ("T", "UR"),
    ("UL", "UR"),
    ("UL", "LL"),
    ("UR", "LR"),
    ("LL", "LR"),
    ("UL", "LR"),
    ("UR", "LL"),
]

# Langues suivies par chaque étudiant (exercice 2 du TD).
COURSE_STUDENTS = {
    "anglais": ["Axel", "Corentin", "Emilie"],
    "russe": ["Béatrice", "Dylan", "Emilie"],
    "espagnol": ["Axel", "Dylan"],
    "italien": ["Corentin"],
    "grec": ["Béatrice"],
}


def petersen_graph() -> Graph:
    return Graph.from_edges(PETERSEN_EDGES)


def envelope_graph() -> Graph:
    return Graph.from_edges(ENVELOPE_EDGES)


def language_bipartite_graph() -> Graph:
    """Étudiants d'un côté, cours de l'autre, une arête par inscription."""
    graph = Graph()
    for course, students in COURSE_STUDENTS.items():
        course_vertex = f"course:{course}"
        graph.add_vertex(course_vertex)
        for student in students:
            graph.add_edge(f"student:{student}", course_vertex)
    return graph


def students_graph() -> Graph:
    """Deux étudiants sont adjacents lorsqu'ils partagent au moins un cours."""
    graph = Graph()
    graph.add_vertices(COURSE_STUDENTS["anglais"] + [
        student for students in COURSE_STUDENTS.values() for student in students
    ])
    students = sorted(graph.vertices)
    for first, second in combinations(students, 2):
        if any(
            first in members and second in members
            for members in COURSE_STUDENTS.values()
        ):
            graph.add_edge(first, second)
    return graph


def course_graph() -> Graph:
    """Deux cours sont adjacents lorsqu'au moins un étudiant suit les deux."""
    graph = Graph()
    graph.add_vertices(COURSE_STUDENTS)
    for first, second in combinations(COURSE_STUDENTS, 2):
        if set(COURSE_STUDENTS[first]) & set(COURSE_STUDENTS[second]):
            graph.add_edge(first, second)
    return graph


def shared_course_pairs() -> list[tuple[str, str]]:
    return sorted(students_graph().edges())
