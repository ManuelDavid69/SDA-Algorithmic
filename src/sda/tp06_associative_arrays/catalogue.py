"""Catalogue de Vinyl Records Co. : index par hachage et index AVL (TP 6)."""

from __future__ import annotations

from dataclasses import dataclass

from .avl import AVLTree
from .hash_table import HashTable


@dataclass(frozen=True)
class VinylRecord:
    """Une fiche du catalogue."""

    reference: str
    title: str
    artist: str
    year: int
    price: float

    def __post_init__(self) -> None:
        if len(self.reference) != 13 or not self.reference.isdigit():
            raise ValueError("une référence de catalogue doit contenir 13 chiffres")
        if not 1900 <= self.year <= 2100:
            raise ValueError("année de publication invalide")
        if self.price < 0:
            raise ValueError("le prix doit être positif ou nul")

    @property
    def key(self) -> int:
        return int(self.reference)


class Catalogue:
    """Deux index sur les mêmes fiches.

    - une table de hachage indexée par la référence numérique, pour les
      recherches exactes ;
    - un arbre AVL indexé par l'année de publication, pour les requêtes par
      intervalle.
    """

    def __init__(self, records: list[VinylRecord] | None = None) -> None:
        self.records: dict[str, VinylRecord] = {}
        self.by_reference = HashTable()
        self.by_year = AVLTree()
        for record in records or []:
            self.add(record)

    def __len__(self) -> int:
        return len(self.records)

    def add(self, record: VinylRecord) -> None:
        if record.reference in self.records:
            raise ValueError(f"référence en double : {record.reference}")
        self.records[record.reference] = record
        self.by_reference.insert(record.key, record)
        self.by_year.insert(record.year, record.reference)

    def price(self, reference: str) -> float:
        record: VinylRecord = self.by_reference.get(int(reference))
        return record.price

    def record(self, reference: str) -> VinylRecord:
        return self.by_reference.get(int(reference))

    def between(self, first_year: int, last_year: int) -> list[VinylRecord]:
        """Toutes les fiches publiées entre deux années, triées par année puis par titre."""
        result: list[VinylRecord] = []
        for _year, references in self.by_year.range_query(first_year, last_year):
            for reference in references:
                result.append(self.records[reference])
        return sorted(result, key=lambda record: (record.year, record.title))
