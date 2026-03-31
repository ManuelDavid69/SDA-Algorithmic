"""Practical work 3: recursion, divide and conquer, Hanoi and search."""

from .hanoi import Move, hanoi, hanoi_moves_text, print_hanoi
from .recursion import (
    fibonacci1,
    fibonacci2,
    fibonacci3,
    max_list,
    numbers_ascending,
    numbers_descending,
    print_ascending,
    print_descending,
)

__all__ = [
    "Move",
    "fibonacci1",
    "fibonacci2",
    "fibonacci3",
    "hanoi",
    "hanoi_moves_text",
    "max_list",
    "numbers_ascending",
    "numbers_descending",
    "print_ascending",
    "print_descending",
    "print_hanoi",
]
