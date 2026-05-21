"""Tests for TP 2: operation counts, growth classes and benchmarks."""

import math

import pytest

from sda.tp02_complexity.benchmarks import (
    complexity_table,
    format_duration,
    is_prime,
    max_instance_sizes,
    measure_prime,
    prime_iterations,
    theoretical_times,
)
from sda.tp02_complexity.counting import (
    program1,
    program1_formula,
    program2,
    program2_formula,
    program3,
    program3_formula,
    program4,
    program4_formula,
    program5,
    program5_formula,
)
from sda.tp02_complexity.growth import (
    FUNCTIONS,
    GROWTH_CLASSES,
    GROWTH_ORDER,
    rank,
    same_class,
    theta_class,
)


@pytest.mark.parametrize("n", range(16))
def test_program1(n):
    result = program1(n)
    assert result.operations == program1_formula(n) == 2 * n + 1
    assert result.value == 0


@pytest.mark.parametrize("n", range(16))
def test_program2(n):
    result = program2(n)
    assert result.operations == program2_formula(n) == n * n + 1
    assert result.value == (n * (n - 1) // 2) ** 2


@pytest.mark.parametrize("n", range(16))
def test_program3(n):
    result = program3(n)
    assert result.operations == program3_formula(n) == 3 * n * n + 3 * n + 3
    assert result.value == 33


@pytest.mark.parametrize("n", range(1, 20))
def test_program4(n):
    result = program4(n)
    assert result.operations == program4_formula(n)
    assert result.operations == 1 + 2 * (n.bit_length())


@pytest.mark.parametrize("n", range(9))
def test_program5(n):
    result = program5(n)
    assert result.operations == program5_formula(n) == 3 * n * n * (n * n + 1) + 1
    assert result.value == 3 * n * n * (n * n + 1)


@pytest.mark.parametrize(
    "program", [program1, program2, program3, program4, program5]
)
def test_programs_reject_negative_sizes(program):
    with pytest.raises(ValueError):
        program(-1)


def test_growth_has_fifteen_functions():
    assert len(FUNCTIONS) == 15
    assert len(set(FUNCTIONS)) == 15
    assert len(GROWTH_ORDER) == 15


def test_growth_order_matches_classes():
    assert GROWTH_ORDER[0] == "6"
    assert GROWTH_ORDER[-1] == "n!"
    assert GROWTH_ORDER.index("lg n") < GROWTH_ORDER.index("n")
    assert GROWTH_ORDER.index("n^2") < GROWTH_ORDER.index("n^3")
    assert GROWTH_ORDER.index("(3/2)^n") < GROWTH_ORDER.index("2^n") < GROWTH_ORDER.index("n!")


def test_same_asymptotic_class():
    assert same_class("2^n", "2^(n-1)")
    assert same_class("n^3", "n^3 + lg n")
    assert same_class("n^3", "n - n^2 + 5n^3")
    assert not same_class("n^2", "n^3")
    assert not same_class("n lg n", "n")
    assert theta_class("n - n^2 + 5n^3") == "Theta(n^3)"
    assert theta_class("sqrt(n)") == "Theta(sqrt(n))"


def test_rank_and_unknown_function():
    assert rank("6") == 0
    assert rank("n!") == 14
    with pytest.raises(KeyError):
        rank("n^42")
    with pytest.raises(KeyError):
        theta_class("n^42")


def test_growth_classes_are_ordered():
    starts = [GROWTH_ORDER.index(member) for group in GROWTH_CLASSES for member in group.members]
    assert starts == sorted(starts)


@pytest.mark.parametrize(
    ("number", "expected"),
    [(0, False), (1, False), (2, True), (3, True), (4, False), (17, True), (25, False), (97, True)],
)
def test_is_prime(number, expected):
    assert is_prime(number) is expected


def test_prime_iterations():
    assert prime_iterations(0) == 0
    assert prime_iterations(2) == 0
    assert prime_iterations(9) == 2
    assert prime_iterations(10_000) == 99


def test_measure_prime():
    measurements = measure_prime([97, 100])
    assert [item.number for item in measurements] == [97, 100]
    assert [item.digits for item in measurements] == [2, 3]
    assert all(item.seconds >= 0 for item in measurements)
    assert measurements[0].iterations == prime_iterations(97)


def test_format_duration_units():
    assert format_duration(0.5e-6) == "500.0 ns"
    assert format_duration(2e-6).endswith("us")
    assert format_duration(2e-3).endswith("ms")
    assert format_duration(2) == "2.00 s"
    assert format_duration(120) == "2.00 min"
    assert format_duration(7200) == "2.00 h"
    assert format_duration(2 * 86400) == "2.00 days"
    assert format_duration(2 * 365 * 86400) == "2.00 years"
    assert "e+" in format_duration(1e9 * 365 * 86400)


def test_theoretical_times():
    times = theoretical_times(10**6)
    assert set(times) == {"log n", "n", "n^2", "2^n"}
    assert times["n"] == "1.00 s"
    assert times["n^2"].endswith("days")
    assert "years" in times["2^n"]


def test_max_instance_sizes_one_second():
    sizes = {item.complexity: item for item in max_instance_sizes(1.0)}
    assert sizes["sqrt(n)"].value == 1000
    assert sizes["n"].value == 1_000_000
    assert sizes["n^2"].value == 1000
    assert sizes["n^3"].value == 100
    assert sizes["2^n"].value == 19
    assert sizes["n!"].value == 9
    assert 60_000 < sizes["n lg n"].value < 70_000
    assert sizes["lg n"].value is None
    assert sizes["lg n"].display.startswith("2^")


def test_max_instance_sizes_respects_the_operation_cost():
    fast = {item.complexity: item.value for item in max_instance_sizes(1.0, operation_seconds=1e-9)}
    assert fast["n"] == 1_000_000_000
    assert fast["n^2"] == 31_622


def test_complexity_table_shape():
    table = complexity_table()
    assert len(table) == 9
    assert len(table[0]) == 8
    assert table[0][0] == "Complexity"
    assert [row[0] for row in table[1:]] == [
        "lg n",
        "sqrt(n)",
        "n",
        "n lg n",
        "n^2",
        "n^3",
        "2^n",
        "n!",
    ]


def test_course_numbers_are_all_odd():
    from sda.tp02_complexity.benchmarks import COURSE_NUMBERS

    assert all(number % 2 == 1 for number in COURSE_NUMBERS)
    assert all(len(str(number)) >= 10 for number in COURSE_NUMBERS)
    assert math.log2(COURSE_NUMBERS[0]) > 30
