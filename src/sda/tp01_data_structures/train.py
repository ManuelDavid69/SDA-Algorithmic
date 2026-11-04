"""Simulation de train reposant sur la liste chaînée (TP 1, exercice 1, questions 3-4)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .linked_list import LinkedList


@dataclass
class Wagon:
    """Un wagon avec une capacité fixe."""

    number: int
    capacity: int = 4
    passengers: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.number < 1:
            raise ValueError("la numérotation des wagons commence à 1")
        if self.capacity < 1:
            raise ValueError("un wagon doit avoir une capacité positive")

    @property
    def is_full(self) -> bool:
        return len(self.passengers) >= self.capacity

    def board(self, passenger: str) -> None:
        if self.is_full:
            raise ValueError(f"le wagon {self.number} est plein")
        self.passengers.append(passenger)

    def alight(self) -> str:
        if not self.passengers:
            raise IndexError(f"le wagon {self.number} est vide")
        return self.passengers.pop()

    def __repr__(self) -> str:
        contents = ", ".join(self.passengers) if self.passengers else "vide"
        return f"Wagon {self.number} ({len(self.passengers)}/{self.capacity}) : {contents}"


class Train:
    """Un train composé d'un nombre fixe de wagons.

    ``board(passenger, k)`` commence au wagon ``k`` et parcourt le train vers
    l'arrière, comme demandé aux questions 1-3.  Avec ``search_backwards=True``
    (question 4), un passager qui ne trouve pas de place après le wagon ``k``
    repart vers l'avant du train avant d'abandonner.
    """

    def __init__(self, wagons: int = 3, capacity: int = 4) -> None:
        if wagons < 1:
            raise ValueError("un train doit comporter au moins un wagon")
        self.wagons: LinkedList = LinkedList(
            Wagon(number, capacity) for number in range(1, wagons + 1)
        )

    def __len__(self) -> int:
        return len(self.wagons)

    def __iter__(self):
        return iter(self.wagons)

    def _wagon(self, k: int) -> Wagon:
        if k < 1 or k > len(self.wagons):
            raise IndexError(f"wagon hors limites : {k}")
        return self.wagons.get(k - 1)

    def board(self, passenger: str, k: int, search_backwards: bool = False) -> int | None:
        """Fait monter ``passenger`` au wagon ``k`` ou après.

        Renvoie le numéro du wagon effectivement emprunté par le passager, ou
        ``None`` lorsque le train est complet.  Lorsque ``search_backwards`` est
        vrai et qu'aucune place n'est trouvée de ``k`` au dernier wagon, la
        recherche se poursuit du premier wagon jusqu'à ``k - 1``.
        """
        self._wagon(k)  # valider k avant toute autre opération
        start = k - 1
        order = list(range(start, len(self.wagons)))
        if search_backwards:
            order += list(range(0, start))
        for index in order:
            wagon = self.wagons.get(index)
            if not wagon.is_full:
                wagon.board(passenger)
                return wagon.number
        return None

    def alight(self, k: int) -> str:
        """Un passager descend du wagon ``k`` ; renvoie son nom."""
        return self._wagon(k).alight()

    def passengers(self) -> list[str]:
        return [name for wagon in self.wagons for name in wagon.passengers]

    def __repr__(self) -> str:
        lines = [repr(wagon) for wagon in self.wagons]
        return "Train:\n" + "\n".join(f"  {line}" for line in lines)
