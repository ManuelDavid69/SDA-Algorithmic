"""Train simulation on top of the linked list (TP 1, exercise 1, questions 3-4)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .linked_list import LinkedList


@dataclass
class Wagon:
    """A wagon with a fixed capacity."""

    number: int
    capacity: int = 4
    passengers: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.number < 1:
            raise ValueError("wagon numbers start at 1")
        if self.capacity < 1:
            raise ValueError("a wagon must have a positive capacity")

    @property
    def is_full(self) -> bool:
        return len(self.passengers) >= self.capacity

    def board(self, passenger: str) -> None:
        if self.is_full:
            raise ValueError(f"wagon {self.number} is full")
        self.passengers.append(passenger)

    def alight(self) -> str:
        if not self.passengers:
            raise IndexError(f"wagon {self.number} is empty")
        return self.passengers.pop()

    def __repr__(self) -> str:
        contents = ", ".join(self.passengers) if self.passengers else "empty"
        return f"Wagon {self.number} ({len(self.passengers)}/{self.capacity}): {contents}"


class Train:
    """A train made of a fixed number of wagons.

    ``board(passenger, k)`` starts at wagon ``k`` and walks towards the end of
    the train, as requested by questions 1-3.  With ``search_backwards=True``
    (question 4), a passenger who finds no room after wagon ``k`` walks back
    towards the front of the train before giving up.
    """

    def __init__(self, wagons: int = 3, capacity: int = 4) -> None:
        if wagons < 1:
            raise ValueError("a train needs at least one wagon")
        self.wagons: LinkedList = LinkedList(
            Wagon(number, capacity) for number in range(1, wagons + 1)
        )

    def __len__(self) -> int:
        return len(self.wagons)

    def __iter__(self):
        return iter(self.wagons)

    def _wagon(self, k: int) -> Wagon:
        if k < 1 or k > len(self.wagons):
            raise IndexError(f"wagon out of range: {k}")
        return self.wagons.get(k - 1)

    def board(self, passenger: str, k: int, search_backwards: bool = False) -> int | None:
        """Board ``passenger`` at wagon ``k`` or later.

        Returns the number of the wagon the passenger actually entered, or
        ``None`` when the train is full.  When ``search_backwards`` is true and
        no room is found from ``k`` to the last wagon, the search continues
        from the first wagon up to ``k - 1``.
        """
        self._wagon(k)  # validate k before doing anything
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
        """A passenger gets off wagon ``k``; return their name."""
        return self._wagon(k).alight()

    def passengers(self) -> list[str]:
        return [name for wagon in self.wagons for name in wagon.passengers]

    def __repr__(self) -> str:
        lines = [repr(wagon) for wagon in self.wagons]
        return "Train:\n" + "\n".join(f"  {line}" for line in lines)
