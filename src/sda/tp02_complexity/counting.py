"""Comptage d'opérations élémentaires pour les cinq programmes du TP 2, exercice 1.

Le cours ignore les instructions de contrôle de boucle (``range`` et le test
qui maintient la variable de boucle dans les bornes).  On compte donc une
opération par ligne d'affectation ou d'arithmétique exécutée, ce qui suffit à
identifier la classe asymptotique.  Chaque fonction renvoie également la valeur
finale du programme afin de vérifier la boucle par rapport à sa forme close.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Count:
    """Nombre d'opérations élémentaires et valeur finale d'un programme."""

    operations: int
    value: int


def program1(n: int) -> Count:
    """Deux boucles indépendantes de ``n`` itérations : ``T(n) = 2n + 1``."""
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    test = 0  # 1 opération
    operations = 1
    for _ in range(n):
        test = test + 1
    operations += n
    for _ in range(n):
        test = test - 1
    operations += n
    return Count(operations, test)


def program2(n: int) -> Count:
    """Deux boucles imbriquées : ``T(n) = n^2 + 1``."""
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    test = 0  # 1 opération
    operations = 1
    for i in range(n):
        for j in range(n):
            test = test + i * j
    operations += n * n
    return Count(operations, test)


def program3(n: int) -> Count:
    """Trois opérations dans la double boucle, trois dans la boucle simple.

    ``T(n) = 3n^2 + 3n + 3``.
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    a, b, c = 5, 6, 10  # 3 opérations
    d = 33
    operations = 3
    _ = c
    for i in range(n):
        for j in range(n):
            x = i * i
            y = j * j
            z = i * j
            _ = (x, y, z)
    operations += 3 * n * n
    for k in range(n):
        w = a * k + 45
        v = b * b
        d = 33
        _ = (w, v, d)
    operations += 3 * n
    return Count(operations, d)


def program4(n: int) -> Count:
    """Boucle de division par deux : ``floor(log2 n) + 1`` itérations, deux opérations chacune."""
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    i = n  # 1 opération
    operations = 1
    while i > 0:
        k = 2 + 2
        i = i // 2
        _ = k
        operations += 2
    return Count(operations, k if n > 0 else 0)


def program5(n: int) -> Count:
    """Triple boucle avec une boucle interne constante.

    ``T(n) = 1 + 6 * (1 + 2 + ... + n^2) = 3n^2(n^2 + 1) + 1``.
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    total = 0  # 1 opération
    operations = 1
    for i in range(1, n * n + 1):
        for _ in range(1, i + 1):
            for _ in range(1, 7):
                total = total + 1
    operations += 6 * n * n * (n * n + 1) // 2
    return Count(operations, total)


def program1_formula(n: int) -> int:
    return 2 * n + 1


def program2_formula(n: int) -> int:
    return n * n + 1


def program3_formula(n: int) -> int:
    return 3 * n * n + 3 * n + 3


def program4_formula(n: int) -> int:
    if n == 0:
        return 1
    return 1 + 2 * (n.bit_length())  # floor(log2 n) + 1 itérations


def program5_formula(n: int) -> int:
    return 3 * n * n * (n * n + 1) + 1
