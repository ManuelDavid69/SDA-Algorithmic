"""Tests de la simulation de train (TP 1, exercice 1, questions 3-4)."""

import pytest

from sda.tp01_data_structures.train import Train, Wagon


def test_wagon_capacity_and_repr():
    wagon = Wagon(1)
    assert not wagon.is_full
    for name in ("a", "b", "c", "d"):
        wagon.board(name)
    assert wagon.is_full
    assert "4/4" in repr(wagon)
    with pytest.raises(ValueError):
        wagon.board("e")
    assert wagon.alight() == "d"
    assert not wagon.is_full


def test_empty_wagon_alight():
    with pytest.raises(IndexError):
        Wagon(2).alight()


def test_train_creation():
    train = Train(wagons=4)
    assert len(train) == 4
    assert [wagon.number for wagon in train] == [1, 2, 3, 4]


@pytest.mark.parametrize("wagons", [0, -1])
def test_train_needs_wagons(wagons):
    with pytest.raises(ValueError):
        Train(wagons=wagons)


def test_board_moves_to_the_next_wagon():
    train = Train(wagons=3, capacity=4)
    for i in range(4):
        assert train.board(f"p{i}", 1) == 1
    # Le premier wagon est plein : le passager passe au wagon 2.
    assert train.board("p4", 1) == 2
    assert train.wagons.get(0).passengers == ["p0", "p1", "p2", "p3"]
    assert train.wagons.get(1).passengers == ["p4"]


def test_board_refuses_when_the_last_wagons_are_full():
    train = Train(wagons=2, capacity=1)
    assert train.board("a", 2) == 2
    assert train.board("b", 2) is None


def test_board_with_backtracking_uses_the_front():
    train = Train(wagons=2, capacity=2)
    train.board("a", 1)
    train.board("b", 2)
    train.board("c", 2)
    assert train.board("d", 2) is None
    assert train.board("d", 2, search_backwards=True) == 1


def test_alight():
    train = Train(wagons=2)
    train.board("alice", 1)
    train.board("bob", 1)
    assert train.alight(1) == "bob"
    assert train.passengers() == ["alice"]


@pytest.mark.parametrize("wagon", [0, 3])
def test_invalid_wagon(wagon):
    train = Train(wagons=2)
    with pytest.raises(IndexError):
        train.board("a", wagon)
    with pytest.raises(IndexError):
        train.alight(wagon)


def test_repr_lists_every_wagon():
    train = Train(wagons=2)
    train.board("alice", 1)
    text = repr(train)
    assert "Wagon 1" in text and "alice" in text
    assert "Wagon 2" in text
