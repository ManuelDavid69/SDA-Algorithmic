"""Classes de croissance asymptotique pour les 15 fonctions du TP 2, exercice 2."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComplexityClass:
    """Un ensemble de fonctions qui croissent toutes au même rythme asymptotique."""

    theta: str
    members: tuple[str, ...]

    def __contains__(self, label: str) -> bool:
        return label in self.members


# Les fonctions sont listées de la croissance la plus lente à la plus rapide.
# ``2^(n-1)`` et ``2^n`` ne diffèrent que d'un facteur constant et partagent donc
# la même classe Theta ; il en va de même pour les trois expressions cubiques.
GROWTH_CLASSES: tuple[ComplexityClass, ...] = (
    ComplexityClass("Theta(1)", ("6",)),
    ComplexityClass("Theta(lg lg n)", ("lg lg n",)),
    ComplexityClass("Theta(lg n)", ("lg n",)),
    ComplexityClass("Theta((lg n)^2)", ("(lg n)^2",)),
    ComplexityClass("Theta(sqrt(n))", ("sqrt(n)",)),
    ComplexityClass("Theta(n)", ("n",)),
    ComplexityClass("Theta(n lg n)", ("n lg n",)),
    ComplexityClass("Theta(n^2)", ("n^2",)),
    ComplexityClass("Theta(n^3)", ("n^3", "n^3 + lg n", "n - n^2 + 5n^3")),
    ComplexityClass("Theta((3/2)^n)", ("(3/2)^n",)),
    ComplexityClass("Theta(2^n)", ("2^(n-1)", "2^n")),
    ComplexityClass("Theta(n!)", ("n!",)),
)

FUNCTIONS: tuple[str, ...] = tuple(
    label for complexity_class in GROWTH_CLASSES for label in complexity_class.members
)

GROWTH_ORDER: tuple[str, ...] = (
    "6",
    "lg lg n",
    "lg n",
    "(lg n)^2",
    "sqrt(n)",
    "n",
    "n lg n",
    "n^2",
    "n^3",
    "n^3 + lg n",
    "n - n^2 + 5n^3",
    "(3/2)^n",
    "2^(n-1)",
    "2^n",
    "n!",
)


def theta_class(label: str) -> str:
    """Renvoie la classe Theta d'une fonction, par exemple ``"Theta(n^2)"``."""
    for complexity_class in GROWTH_CLASSES:
        if label in complexity_class:
            return complexity_class.theta
    raise KeyError(f"fonction inconnue : {label!r}")


def same_class(first: str, second: str) -> bool:
    return theta_class(first) == theta_class(second)


def rank(label: str) -> int:
    """Position d'une fonction dans l'ordre de croissance (0 est la plus lente)."""
    try:
        return GROWTH_ORDER.index(label)
    except ValueError as error:
        raise KeyError(f"fonction inconnue : {label!r}") from error
