"""Travaux pratiques 7 : représentations des graphes et algorithmes de base."""

from .analysis import (
    ambassadors_possible,
    ambassadors_report,
    envelope_report,
    petersen_report,
    scheduling_report,
)
from .examples import (
    COURSE_STUDENTS,
    ENVELOPE_EDGES,
    PETERSEN_EDGES,
    course_graph,
    envelope_graph,
    language_bipartite_graph,
    petersen_graph,
    shared_course_pairs,
    students_graph,
)
from .graph import Graph

__all__ = [
    "COURSE_STUDENTS",
    "ENVELOPE_EDGES",
    "PETERSEN_EDGES",
    "Graph",
    "ambassadors_possible",
    "ambassadors_report",
    "course_graph",
    "envelope_graph",
    "envelope_report",
    "language_bipartite_graph",
    "petersen_graph",
    "petersen_report",
    "scheduling_report",
    "shared_course_pairs",
    "students_graph",
]
