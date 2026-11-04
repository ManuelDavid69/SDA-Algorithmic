"""Tours de Hanoï (TP 3, exercice 4)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    """Un déplacement d'un disque de ``source`` vers ``target``."""

    source: int
    target: int

    def __str__(self) -> str:
        return f"Déplacer un disque du piquet {self.source} vers le piquet {self.target}"


def hanoi(n: int, source: int = 1, target: int = 3, auxiliary: int = 2) -> list[Move]:
    """Renvoie la liste des déplacements qui résout les tours de Hanoï.

    La récurrence est ``T(n) = 2 T(n-1) + 1``, d'où ``2^n - 1`` déplacements.
    """
    if n < 0:
        raise ValueError("le nombre de disques doit être positif ou nul")
    if len({source, target, auxiliary}) != 3:
        raise ValueError("les trois piquets doivent être distincts")
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
    """Identique à :func:`hanoi`, mais avec la phrase imprimée dans l'énoncé."""
    return [str(move) for move in hanoi(n)]


def print_hanoi(n: int, output=print) -> None:
    for move in hanoi(n):
        output(str(move))
