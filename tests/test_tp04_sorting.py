"""Tests des algorithmes de tri et de la distribution de bonbons (TP 4)."""

import random

import pytest

from sda.tp04_sorting.candies import best_distribution, brute_force
from sda.tp04_sorting.merge import merge, merge_sort
from sda.tp04_sorting.selection import selection_sort
from sda.tp04_sorting.thirds import thirds_sort


def _random_lists():
    random.seed(20251006)
    lists = [
        [],
        [1],
        [2, 1],
        [1, 2],
        [5, 5, 5],
        [3, 1, 2],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [0, -1, 4, -10, 8, 3, 3],
    ]
    for size in (10, 25, 50, 101):
        lists.append([random.randint(-50, 50) for _ in range(size)])
    return lists


@pytest.mark.parametrize("items", _random_lists())
def test_selection_sort(items):
    original = list(items)
    result = selection_sort(items)
    assert result is items
    assert result == sorted(original)


@pytest.mark.parametrize("items", _random_lists())
def test_merge_sort(items):
    original = list(items)
    result = merge_sort(items)
    assert result == sorted(original)
    assert items == original  # le tri fusion construit une nouvelle liste


@pytest.mark.parametrize("items", _random_lists())
def test_thirds_sort(items):
    original = list(items)
    result = thirds_sort(items)
    assert result is items
    assert result == sorted(original)


def test_merge_helper():
    assert merge([], []) == []
    assert merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge([1, 2, 3], []) == [1, 2, 3]
    assert merge([], [1, 2]) == [1, 2]
    assert merge([1, 1], [1, 2]) == [1, 1, 1, 2]


def test_thirds_sort_base_cases():
    assert thirds_sort([]) == []
    assert thirds_sort([1]) == [1]
    assert thirds_sort([2, 1]) == [1, 2]
    assert thirds_sort([1, 2]) == [1, 2]


def test_thirds_sort_three_elements():
    for permutation in ([1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]):
        assert thirds_sort(list(permutation)) == [1, 2, 3]


def test_candy_example():
    packets = [7, 3, 2, 9, 12, 5]
    difference, choice = best_distribution(packets, 3)
    assert difference == 3
    assert len(choice) == 3
    assert max(choice) - min(choice) == 3


@pytest.mark.parametrize(
    ("packets", "children", "expected"),
    [
        ([10], 1, 0),
        ([1, 2, 3, 4], 2, 1),
        ([1, 100, 101, 102], 3, 2),
        ([5, 5, 5, 5], 2, 0),
    ],
)
def test_candy_known_cases(packets, children, expected):
    assert best_distribution(packets, children)[0] == expected
    assert brute_force(packets, children)[0] == expected


def test_candy_efficient_matches_brute_force():
    random.seed(20251007)
    for _ in range(50):
        size = random.randint(1, 11)
        packets = [random.randint(0, 30) for _ in range(size)]
        children = random.randint(1, size)
        brute = brute_force(packets, children)
        efficient = best_distribution(packets, children)
        assert efficient[0] == brute[0]
        assert len(efficient[1]) == children
        assert all(packet in packets for packet in efficient[1])


@pytest.mark.parametrize("children", [0, -1, 4])
def test_candy_invalid_number_of_children(children):
    with pytest.raises(ValueError):
        best_distribution([1, 2, 3], children)
    with pytest.raises(ValueError):
        brute_force([1, 2, 3], children)


def test_candy_rejects_negative_packets():
    with pytest.raises(ValueError):
        best_distribution([1, -2, 3], 2)
