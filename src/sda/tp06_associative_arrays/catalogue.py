"""Vinyl Records Co. catalogue: hash index and AVL index (TP 6)."""

from __future__ import annotations

from dataclasses import dataclass

from .avl import AVLTree
from .hash_table import HashTable


@dataclass(frozen=True)
class VinylRecord:
    """A record of the catalogue."""

    reference: str
    title: str
    artist: str
    year: int
    price: float

    def __post_init__(self) -> None:
        if len(self.reference) != 13 or not self.reference.isdigit():
            raise ValueError("a catalogue reference must contain 13 digits")
        if not 1900 <= self.year <= 2100:
            raise ValueError("invalid publication year")
        if self.price < 0:
            raise ValueError("the price must be non-negative")

    @property
    def key(self) -> int:
        return int(self.reference)


class Catalogue:
    """Two indexes over the same records.

    - a hash table keyed by the numeric reference, for exact lookups;
    - an AVL tree keyed by the publication year, for range queries.
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
            raise ValueError(f"duplicate reference: {record.reference}")
        self.records[record.reference] = record
        self.by_reference.insert(record.key, record)
        self.by_year.insert(record.year, record.reference)

    def price(self, reference: str) -> float:
        record: VinylRecord = self.by_reference.get(int(reference))
        return record.price

    def record(self, reference: str) -> VinylRecord:
        return self.by_reference.get(int(reference))

    def between(self, first_year: int, last_year: int) -> list[VinylRecord]:
        """All records published between two years, sorted by year and title."""
        result: list[VinylRecord] = []
        for _year, references in self.by_year.range_query(first_year, last_year):
            for reference in references:
                result.append(self.records[reference])
        return sorted(result, key=lambda record: (record.year, record.title))
