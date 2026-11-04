"""Liste simplement chaînée, écrite de zéro (TP 1, exercice 1)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    """Un nœud d'une liste simplement chaînée."""

    value: Any
    next: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class LinkedList:
    """Une liste simplement chaînée avec un pointeur de tête.

    Les positions sont indexées à partir de 0.  Toutes les opérations qui
    parcourent la liste sont en ``O(k)`` (ou ``O(n)``) ; l'insertion et la
    suppression en tête sont en ``O(1)``.
    """

    def __init__(self, values: Iterable[Any] | None = None) -> None:
        self.head: Node | None = None
        self._size = 0
        if values is not None:
            self.extend(values)

    # ------------------------------------------------------------------
    # Taille et représentation
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return not self.is_empty()

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return " -> ".join(repr(value) for value in self) + " -> None"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LinkedList):
            return self.to_list() == other.to_list()
        if isinstance(other, list):
            return self.to_list() == other
        return NotImplemented

    def to_list(self) -> list[Any]:
        return list(self)

    # ------------------------------------------------------------------
    # Opérations principales
    # ------------------------------------------------------------------
    def append(self, value: Any) -> None:
        """Ajoute ``value`` à la fin de la liste."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def extend(self, values: Iterable[Any]) -> None:
        for value in values:
            self.append(value)

    def insert(self, value: Any, k: int) -> None:
        """Insère ``value`` à la position ``k`` (``0 <= k <= size``)."""
        if k < 0 or k > self._size:
            raise IndexError(f"position d'insertion hors limites : {k}")
        node = Node(value)
        if k == 0:
            node.next = self.head
            self.head = node
        else:
            previous = self._node_at(k - 1)
            node.next = previous.next
            previous.next = node
        self._size += 1

    def delete(self, k: int) -> Any:
        """Retire et renvoie la valeur située à la position ``k``."""
        self._check_index(k)
        if k == 0:
            assert self.head is not None
            removed = self.head.value
            self.head = self.head.next
        else:
            previous = self._node_at(k - 1)
            assert previous.next is not None
            removed = previous.next.value
            previous.next = previous.next.next
        self._size -= 1
        return removed

    def search(self, value: Any) -> int:
        """Renvoie l'indice de la première occurrence de ``value``, ou ``-1``."""
        index = 0
        current = self.head
        while current is not None:
            if current.value == value:
                return index
            index += 1
            current = current.next
        return -1

    def get(self, k: int) -> Any:
        """Renvoie la valeur située à la position ``k``."""
        return self._node_at(k).value

    def __getitem__(self, k: int) -> Any:
        return self.get(k)

    def __setitem__(self, k: int, value: Any) -> None:
        self._node_at(k).value = value

    # ------------------------------------------------------------------
    # Fonctions auxiliaires
    # ------------------------------------------------------------------
    def _check_index(self, k: int) -> None:
        if k < 0 or k >= self._size:
            raise IndexError(f"indice de liste hors limites : {k}")

    def _node_at(self, k: int) -> Node:
        self._check_index(k)
        current = self.head
        assert current is not None
        for _ in range(k):
            assert current.next is not None
            current = current.next
        return current

    def clear(self) -> None:
        self.head = None
        self._size = 0
