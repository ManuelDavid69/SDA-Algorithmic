"""Tests for the linked list (TP 1, exercise 1)."""

import pytest

from sda.tp01_data_structures.linked_list import LinkedList, Node


def test_node_repr():
    assert repr(Node(42)) == "Node(42)"


def test_empty_list():
    lst = LinkedList()
    assert lst.is_empty()
    assert lst.size == 0
    assert len(lst) == 0
    assert lst.to_list() == []
    assert repr(lst) == " -> None"


def test_build_from_iterable_and_repr():
    lst = LinkedList([1, 2, 3])
    assert lst.to_list() == [1, 2, 3]
    assert lst.size == 3
    assert repr(lst) == "1 -> 2 -> 3 -> None"
    assert list(lst) == [1, 2, 3]


def test_append_keeps_order():
    lst = LinkedList()
    for value in ("a", "b", "c"):
        lst.append(value)
    assert lst.to_list() == ["a", "b", "c"]
    assert not lst.is_empty()


def test_insert_at_every_position():
    lst = LinkedList([1, 2, 3])
    lst.insert(0, 0)
    assert lst.to_list() == [0, 1, 2, 3]
    lst.insert(99, 2)
    assert lst.to_list() == [0, 1, 99, 2, 3]
    lst.insert(4, len(lst))
    assert lst.to_list() == [0, 1, 99, 2, 3, 4]


@pytest.mark.parametrize("position", [-1, 4])
def test_insert_out_of_range(position):
    lst = LinkedList([1, 2, 3])
    with pytest.raises(IndexError):
        lst.insert(0, position)


def test_delete_head_middle_tail():
    lst = LinkedList([10, 20, 30, 40])
    assert lst.delete(0) == 10
    assert lst.delete(1) == 30
    assert lst.delete(1) == 40
    assert lst.to_list() == [20]
    assert lst.delete(0) == 20
    assert lst.is_empty()


@pytest.mark.parametrize("position", [-1, 3])
def test_delete_out_of_range(position):
    lst = LinkedList([1, 2, 3])
    with pytest.raises(IndexError):
        lst.delete(position)


def test_search():
    lst = LinkedList(["a", "b", "a"])
    assert lst.search("a") == 0
    assert lst.search("b") == 1
    assert lst.search("z") == -1


def test_get_and_set():
    lst = LinkedList([5, 6, 7])
    assert lst.get(0) == 5
    assert lst.get(2) == 7
    assert lst[1] == 6
    lst[1] = 60
    assert lst.to_list() == [5, 60, 7]


@pytest.mark.parametrize("position", [-1, 3])
def test_get_out_of_range(position):
    lst = LinkedList([1, 2, 3])
    with pytest.raises(IndexError):
        lst.get(position)


def test_clear():
    lst = LinkedList([1, 2])
    lst.clear()
    assert lst.is_empty()
    assert lst.to_list() == []


def test_equality():
    assert LinkedList([1, 2]) == LinkedList([1, 2])
    assert LinkedList([1, 2]) == [1, 2]
    assert LinkedList([1, 2]) != LinkedList([2, 1])
