"""Fonctions récursives du TP 3 : affichages, Fibonacci et diviser pour régner."""

from __future__ import annotations

from collections.abc import Callable, Iterable


def numbers_ascending(n: int) -> list[int]:
    """Renvoie ``[1, 2, ..., n]`` à l'aide d'une définition récursive."""
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    if n == 0:
        return []
    return numbers_ascending(n - 1) + [n]


def numbers_descending(n: int) -> list[int]:
    """Renvoie ``[n, n-1, ..., 1]`` à l'aide d'une définition récursive."""
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    if n == 0:
        return []
    return [n] + numbers_descending(n - 1)


def print_ascending(n: int, output: Callable[[int], None] = print) -> None:
    """Affiche les nombres de 1 à ``n`` par ordre croissant."""
    if n <= 0:
        return
    print_ascending(n - 1, output)
    output(n)


def print_descending(n: int, output: Callable[[int], None] = print) -> None:
    """Affiche les nombres de ``n`` à 1 par ordre décroissant."""
    if n <= 0:
        return
    output(n)
    print_descending(n - 1, output)


def fibonacci1(n: int) -> int:
    """Fibonacci récursif naïf, avec ``F(0) = F(1) = 1``.

    Le nombre d'appels est exponentiel : ``T(n) = T(n-1) + T(n-2) + 1``.
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    if n <= 1:
        return 1
    return fibonacci1(n - 1) + fibonacci1(n - 2)


def fibonacci2(n: int) -> int:
    """Fibonacci mémoïsé : chaque valeur n'est calculée qu'une fois (``O(n)``)."""
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    cache: dict[int, int] = {0: 1, 1: 1}

    def fib(k: int) -> int:
        if k not in cache:
            cache[k] = fib(k - 1) + fib(k - 2)
        return cache[k]

    return fib(n)


def fibonacci3(n: int) -> int:
    """Fibonacci récursif terminal avec deux accumulateurs.

    La fonction auxiliaire transporte ``(F(k), F(k+1))`` sous la forme ``(a, b)``
    et remplace le couple par ``(b, a + b)`` à chaque appel, de sorte que la
    récursion est terminale et utilise un temps ``O(n)`` et un état arithmétique
    supplémentaire ``O(1)``.
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")

    def fib(k: int, a: int, b: int) -> int:
        if k == 0:
            return a
        return fib(k - 1, b, a + b)

    return fib(n, 1, 1)


def max_list(values: Iterable[int]) -> int:
    """Maximum d'une liste, calculé selon une stratégie de diviser pour régner."""
    items = list(values)
    if not items:
        raise ValueError("l'argument de max_list() est une séquence vide")
    return _max_range(items, 0, len(items))


def _max_range(items: list[int], start: int, end: int) -> int:
    if end - start == 1:
        return items[start]
    middle = (start + end) // 2
    left = _max_range(items, start, middle)
    right = _max_range(items, middle, end)
    return left if left >= right else right
