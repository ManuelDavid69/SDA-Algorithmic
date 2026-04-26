"""Demonstration of TP 6: hash table, AVL tree and vinyl catalogue."""

from __future__ import annotations

from ..tp05_trees.tree_printer import render_tree
from .avl import AVLTree
from .catalogue import Catalogue, VinylRecord
from .hash_table import HashTable

KEYS = [
    9_782_010_000_000,
    9_782_210_000_000,
    9_782_210_000_137,
    9_782_010_138_233,
    9_782_210_000_274,
    9_782_010_276_466,
]

RECORDS = [
    VinylRecord("9782010000000", "Abbey Road", "The Beatles", 1969, 24.99),
    VinylRecord("9782210000000", "Kind of Blue", "Miles Davis", 1959, 19.99),
    VinylRecord("9782210000137", "A Love Supreme", "John Coltrane", 1965, 21.50),
    VinylRecord("9782010138233", "Pet Sounds", "The Beach Boys", 1966, 22.00),
    VinylRecord("9782210000274", "Bitches Brew", "Miles Davis", 1970, 27.00),
    VinylRecord("9782010276466", "The Dark Side of the Moon", "Pink Floyd", 1973, 25.00),
    VinylRecord("9782010999999", "Wish You Were Here", "Pink Floyd", 1975, 23.00),
]


def main() -> None:
    print("== Hash table (m = 1009) ==")
    table = HashTable()
    for key in KEYS:
        probes = table.insert(key, key)
        print(f"{key}: h(k) = {key % 1009:>3}, extra probes = {probes}, slot = {table.slot_of(key)}")
    print(f"load factor for {len(table)} keys: {table.load_factor:.4f}")
    print(f"theoretical load factor for 700 keys: {700 / 1009:.4f}")

    print("\n== Deletion with a DELETED tombstone ==")
    small = HashTable(size=7)
    for key in (1, 8, 15):
        small.insert(key, key)
    print("after inserting 1, 8, 15: slots 1, 2 and 3")
    small.delete(8)
    print(f"after deleting 8, get(15) = {small.get(15)} (the search skips the tombstone)")
    small.insert(22, 22)
    print(f"inserting 22 reuses slot {small.slot_of(22)}; get(15) still returns {small.get(15)}")

    print("\n== AVL tree ==")
    tree = AVLTree()
    for year in (66, 72, 69, 58, 80, 75):
        tree.insert(year)
        print(f"insert {year}: rotations = {tree.rotations}, height = {tree.height()}")
    print(render_tree(tree.root))
    print(f"in-order: {tree.in_order()}")
    print(f"balance factors: {tree.balance_factors()}")
    print(f"range 60..76: {tree.range_query(60, 76)}")

    print("\n== Vinyl Records Co. catalogue ==")
    catalogue = Catalogue(RECORDS)
    print(f"price of 9782010000000: {catalogue.price('9782010000000')} EUR")
    print("records published between 1965 and 1975:")
    for record in catalogue.between(1965, 1975):
        print(f"  {record.year} - {record.artist} - {record.title} ({record.price:.2f} EUR)")


if __name__ == "__main__":
    main()
