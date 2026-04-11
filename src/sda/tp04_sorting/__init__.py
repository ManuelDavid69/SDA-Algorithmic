"""Practical work 4: selection sort, merge sort, two-thirds sort and candies."""

from .candies import best_distribution, brute_force
from .merge import merge, merge_sort
from .selection import selection_sort
from .thirds import thirds_sort

__all__ = [
    "best_distribution",
    "brute_force",
    "merge",
    "merge_sort",
    "selection_sort",
    "thirds_sort",
]
