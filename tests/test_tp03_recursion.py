"""Tests de la récursivité, de Fibonacci, de diviser pour régner et de Hanoi (TP 3)."""

import pytest

from sda.tp03_recursion.hanoi import Move, hanoi, hanoi_moves_text, print_hanoi
from sda.tp03_recursion.recursion import (
    fibonacci1,
    fibonacci2,
    fibonacci3,
    max_list,
    numbers_ascending,
    numbers_descending,
    print_ascending,
    print_descending,
)
from sda.tp03_recursion.search import (
    binary_search_iterative,
    binary_search_recursive,
    dicho,
    linear_search,
)


@pytest.mark.parametrize(("n", "ascending", "descending"), [
    (0, [], []),
    (1, [1], [1]),
    (5, [1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
])
def test_numbers(n, ascending, descending):
    assert numbers_ascending(n) == ascending
    assert numbers_descending(n) == descending


def test_negative_number_of_values():
    with pytest.raises(ValueError):
        numbers_ascending(-1)
    with pytest.raises(ValueError):
        numbers_descending(-1)


def test_print_ascending_and_descending():
    output: list[int] = []
    print_ascending(4, output.append)
    assert output == [1, 2, 3, 4]
    output.clear()
    print_descending(4, output.append)
    assert output == [4, 3, 2, 1]
    output.clear()
    print_ascending(0, output.append)
    assert output == []


@pytest.mark.parametrize("n", range(21))
def test_fibonacci_variants_agree(n):
    expected = fibonacci1(n)
    assert fibonacci2(n) == expected
    assert fibonacci3(n) == expected


def test_fibonacci_first_values():
    assert [fibonacci1(n) for n in range(8)] == [1, 1, 2, 3, 5, 8, 13, 21]
    assert [fibonacci3(n) for n in range(8)] == [1, 1, 2, 3, 5, 8, 13, 21]


@pytest.mark.parametrize("function", [fibonacci1, fibonacci2, fibonacci3])
def test_fibonacci_rejects_negative(function):
    with pytest.raises(ValueError):
        function(-1)


def test_max_list():
    assert max_list([3]) == 3
    assert max_list([1, 9, 4, 7, 2]) == 9
    assert max_list([-5, -2, -9]) == -2
    assert max_list(range(100)) == 99
    with pytest.raises(ValueError):
        max_list([])


def test_hanoi_move_count():
    for n in range(10):
        assert len(hanoi(n)) == 2**n - 1


def test_hanoi_three_disks():
    expected = [
        Move(1, 3),
        Move(1, 2),
        Move(3, 2),
        Move(1, 3),
        Move(2, 1),
        Move(2, 3),
        Move(1, 3),
    ]
    assert hanoi(3) == expected


def test_hanoi_moves_are_legal():
    pegs: dict[int, list[int]] = {1: list(range(5, 0, -1)), 2: [], 3: []}
    for move in hanoi(5):
        disk = pegs[move.source].pop()
        if pegs[move.target]:
            assert disk < pegs[move.target][-1]
        pegs[move.target].append(disk)
    assert pegs[3] == [5, 4, 3, 2, 1]


def test_hanoi_text_and_print(capsys):
    assert hanoi_moves_text(1) == ["Déplacer un disque du piquet 1 vers le piquet 3"]
    print_hanoi(2)
    captured = capsys.readouterr().out
    assert captured.count("Déplacer un disque") == 3


def test_hanoi_rejects_invalid_arguments():
    with pytest.raises(ValueError):
        hanoi(-1)
    with pytest.raises(ValueError):
        hanoi(2, source=1, target=1, auxiliary=2)


def test_linear_search():
    items = [4, 8, 15, 16, 23, 42]
    assert linear_search(items, 4) == 0
    assert linear_search(items, 23) == 4
    assert linear_search(items, 42) == 5
    assert linear_search(items, 7) == -1
    assert linear_search([], 1) == -1


def test_binary_search_all_positions():
    items = list(range(0, 101, 3))
    for index, value in enumerate(items):
        assert binary_search_recursive(items, value) == index
        assert binary_search_iterative(items, value) == index
        assert dicho(items, value) == index


def test_binary_search_absent_values():
    items = [1, 3, 5, 7, 9]
    for target in (-1, 0, 2, 4, 6, 8, 10):
        assert binary_search_recursive(items, target) == -1
        assert binary_search_iterative(items, target) == -1


def test_binary_search_empty_and_singleton():
    assert binary_search_recursive([], 3) == -1
    assert binary_search_iterative([], 3) == -1
    assert binary_search_recursive([3], 3) == 0
    assert binary_search_iterative([3], 3) == 0
    assert binary_search_recursive([3], 4) == -1
    assert binary_search_iterative([3], 4) == -1
