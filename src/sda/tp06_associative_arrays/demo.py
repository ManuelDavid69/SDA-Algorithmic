"""Démonstration du TP 6 : table de hachage, arbre AVL et catalogue de vinyles."""

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
    print("== Table de hachage (m = 1009) ==")
    table = HashTable()
    for key in KEYS:
        probes = table.insert(key, key)
        print(
            f"{key}: h(k) = {key % 1009:>3}, sondages supplémentaires = {probes}, "
            f"emplacement = {table.slot_of(key)}"
        )
    print(f"taux de remplissage pour {len(table)} clés : {table.load_factor:.4f}")
    print(f"taux de remplissage théorique pour 700 clés : {700 / 1009:.4f}")

    print("\n== Suppression avec une pierre tombale DELETED ==")
    small = HashTable(size=7)
    for key in (1, 8, 15):
        small.insert(key, key)
    print("après insertion de 1, 8, 15 : emplacements 1, 2 et 3")
    small.delete(8)
    print(
        f"après suppression de 8, get(15) = {small.get(15)} "
        "(la recherche saute la pierre tombale)"
    )
    small.insert(22, 22)
    print(
        f"l'insertion de 22 réutilise l'emplacement {small.slot_of(22)} ; "
        f"get(15) renvoie toujours {small.get(15)}"
    )

    print("\n== Arbre AVL ==")
    tree = AVLTree()
    for year in (66, 72, 69, 58, 80, 75):
        tree.insert(year)
        print(f"insertion de {year} : rotations = {tree.rotations}, hauteur = {tree.height()}")
    print(render_tree(tree.root))
    print(f"parcours infixe : {tree.in_order()}")
    print(f"facteurs d'équilibre : {tree.balance_factors()}")
    print(f"intervalle 60..76 : {tree.range_query(60, 76)}")

    print("\n== Catalogue de Vinyl Records Co. ==")
    catalogue = Catalogue(RECORDS)
    print(f"prix de 9782010000000 : {catalogue.price('9782010000000')} EUR")
    print("fiches publiées entre 1965 et 1975 :")
    for record in catalogue.between(1965, 1975):
        print(f"  {record.year} - {record.artist} - {record.title} ({record.price:.2f} EUR)")


if __name__ == "__main__":
    main()
