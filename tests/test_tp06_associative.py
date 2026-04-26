"""Tests for TP 6: hash table, AVL tree and vinyl catalogue."""

import pytest

from sda.tp06_associative_arrays.avl import AVLTree
from sda.tp06_associative_arrays.catalogue import Catalogue, VinylRecord
from sda.tp06_associative_arrays.hash_table import HashTable

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


def test_hash_slots_and_collisions():
    table = HashTable()
    probes = [table.insert(key, key) for key in KEYS]
    assert [key % 1009 for key in KEYS] == [335, 391, 528, 335, 665, 335]
    assert probes == [0, 0, 0, 1, 0, 2]
    assert [table.slot_of(key) for key in KEYS] == [335, 391, 528, 336, 665, 337]
    assert len(table) == 6
    assert table.load_factor == pytest.approx(6 / 1009)


def test_hash_get_update_and_delete():
    table = HashTable(size=11)
    table.insert(1, "one")
    table.insert(12, "twelve")
    table.insert(23, "twenty-three")
    assert table.get(1) == "one"
    assert table.get(12) == "twelve"
    assert 12 in table
    assert table.insert(12, "TWELVE") == 1
    assert table.get(12) == "TWELVE"
    assert len(table) == 3
    assert table.delete(12) == "TWELVE"
    assert 12 not in table
    with pytest.raises(KeyError):
        table.get(12)
    assert table.get(23) == "twenty-three"


def test_hash_deletion_leaves_a_tombstone():
    # 1, 8 and 15 all hash to slot 1 in a table of size 7.
    table = HashTable(size=7)
    for key in (1, 8, 15):
        table.insert(key, key)
    assert table.slot_of(15) == 3
    table.delete(8)
    # With a naive None deletion, the search for 15 would stop at slot 2.
    assert table.get(15) == 15
    assert table.slot_of(15) == 3
    assert table.insert(22, 22) == 3
    assert table.slot_of(22) == 2  # the tombstone is reused
    assert table.get(15) == 15
    assert table.get(22) == 22


def test_hash_full_table():
    table = HashTable(size=3)
    for key in (1, 4, 7):
        table.insert(key, key)
    assert len(table) == 3
    with pytest.raises(OverflowError):
        table.insert(10, 10)


def test_hash_invalid_arguments():
    with pytest.raises(ValueError):
        HashTable(size=0)
    table = HashTable(size=5)
    with pytest.raises(TypeError):
        table.insert("not an int", 1)
    with pytest.raises(KeyError):
        table.delete(4)


def test_hash_keys_and_items():
    table = HashTable(size=5)
    table.insert(1, "a")
    table.insert(6, "b")
    assert sorted(table.keys()) == [1, 6]
    assert sorted(table.items()) == [(1, "a"), (6, "b")]


def test_avl_insertion_sequence():
    tree = AVLTree()
    for year in (66, 72, 69, 58, 80, 75):
        tree.insert(year)
    assert tree.in_order() == [58, 66, 69, 72, 75, 80]
    assert tree.height() == 3
    assert tree.rotations == ["RL", "RL"]
    assert tree.is_balanced()
    assert tree.balance_factors() == {
        69: 0,
        66: 1,
        58: 0,
        75: 0,
        72: 0,
        80: 0,
    }
    assert tree.root is not None and tree.root.key == 69


@pytest.mark.parametrize(
    ("values", "rotation"),
    [
        ([30, 20, 10], "LL"),
        ([10, 20, 30], "RR"),
        ([30, 10, 20], "LR"),
        ([10, 30, 20], "RL"),
    ],
)
def test_avl_rotation_types(values, rotation):
    tree = AVLTree()
    for value in values:
        tree.insert(value)
    assert tree.rotations == [rotation]
    assert tree.root is not None and tree.root.key == 20
    assert tree.height() == 2
    assert tree.is_balanced()


def test_avl_references_and_search():
    tree = AVLTree()
    tree.insert(1969, "9782010000000")
    tree.insert(1969, "9782010000001")
    tree.insert(1973, "9782010276466")
    assert tree.search(1969) == ["9782010000000", "9782010000001"]
    assert tree.search(2000) is None
    assert tree.range_query(1960, 1975) == [
        (1969, ["9782010000000", "9782010000001"]),
        (1973, ["9782010276466"]),
    ]
    assert tree.range_query(1970, 1972) == []
    assert tree.range_query(1980, 1960) == []


def test_avl_random_insertions_stay_balanced():
    import random

    random.seed(20251020)
    values = random.sample(range(1000), 200)
    tree = AVLTree()
    for value in values:
        tree.insert(value)
    assert tree.in_order() == sorted(values)
    assert tree.height() <= 2 * (len(values).bit_length())
    assert tree.is_balanced()
    assert len(tree) == len(values)


def test_avl_empty():
    tree = AVLTree()
    assert tree.height() == 0
    assert tree.in_order() == []
    assert tree.items() == []
    assert tree.search(1) is None
    assert tree.range_query(1, 10) == []
    assert tree.is_balanced()
    assert tree.balance_factors() == {}


def test_catalogue_lookup_and_range():
    catalogue = Catalogue(RECORDS)
    assert len(catalogue) == len(RECORDS)
    assert catalogue.price("9782010000000") == 24.99
    assert catalogue.record("9782210000137").title == "A Love Supreme"
    with pytest.raises(KeyError):
        catalogue.price("9782010000001")

    between = catalogue.between(1965, 1975)
    assert [record.title for record in between] == [
        "A Love Supreme",
        "Pet Sounds",
        "Abbey Road",
        "Bitches Brew",
        "The Dark Side of the Moon",
        "Wish You Were Here",
    ]
    assert [record.year for record in between] == [1965, 1966, 1969, 1970, 1973, 1975]


def test_catalogue_rejects_duplicates_and_invalid_records():
    catalogue = Catalogue(RECORDS)
    with pytest.raises(ValueError):
        catalogue.add(RECORDS[0])
    with pytest.raises(ValueError):
        VinylRecord("123", "x", "y", 1970, 1.0)
    with pytest.raises(ValueError):
        VinylRecord("9782010000002", "x", "y", 1800, 1.0)
    with pytest.raises(ValueError):
        VinylRecord("9782010000003", "x", "y", 1970, -1.0)
