"""Towers of Hanoi (TP 3, exercise 4)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    """A move of one disk from ``source`` to ``target``."""

    source: int
    target: int

    def __str__(self) -> str:
        return f"Move a disk from peg {self.source} to peg {self.target}"


def hanoi(n: int, source: int = 1, target: int = 3, auxiliary: int = 2) -> list[Move]:
    """Return the list of moves that solves the Towers of Hanoi.

    The recurrence is ``T(n) = 2 T(n-1) + 1``, hence ``2^n - 1`` moves.
    """
    if n < 0:
        raise ValueError("the number of disks must be non-negative")
    if len({source, target, auxiliary}) != 3:
        raise ValueError("the three pegs must be distinct")
    moves: list[Move] = []

    def solve(disks: int, start: int, end: int, spare: int) -> None:
        if disks == 0:
            return
        solve(disks - 1, start, spare, end)
        moves.append(Move(start, end))
        solve(disks - 1, spare, end, start)

    solve(n, source, target, auxiliary)
    return moves


def hanoi_moves_text(n: int) -> list[str]:
    """Same as :func:`hanoi`, but with the sentence printed in the statement."""
    return [str(move) for move in hanoi(n)]


def print_hanoi(n: int, output=print) -> None:
    for move in hanoi(n):
        output(str(move))
