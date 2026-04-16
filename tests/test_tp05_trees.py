"""Tests for TP 5: BST, tree rendering, expression and ternary trees, Akinator."""

import pytest

from sda.tp05_trees.akinator import Akinator, AnimalNode
from sda.tp05_trees.bst import BST, BSTNode
from sda.tp05_trees.expression_tree import (
    build_from_rpn,
    evaluate,
    evaluate_rpn,
    height,
    to_infix,
    to_postfix,
)
from sda.tp05_trees.ternary import evaluate_ternary, parse_ternary, to_ternary
from sda.tp05_trees.tree_printer import render_tree, tree_lines

VALUES = [25, 60, 35, 10, 5, 20, 65, 45, 70, 40, 50, 55, 30, 15]


def test_bst_insertion_and_in_order():
    tree = BST.build(VALUES)
    assert tree.in_order() == sorted(VALUES)
    assert len(tree) == len(VALUES)
    assert tree.root is not None and tree.root.key == 25
    assert tree.is_valid()


def test_bst_rejects_duplicates():
    tree = BST.build([5, 3, 5, 5])
    assert tree.in_order() == [3, 5]
    assert len(tree) == 2


def test_bst_search():
    tree = BST.build(VALUES)
    for value in VALUES:
        assert tree.search(value)
        assert value in tree
    for value in (0, 1, 26, 64, 100):
        assert not tree.search(value)
        assert value not in tree


def test_bst_minimum_maximum():
    tree = BST.build(VALUES)
    assert tree.minimum() == 5
    assert tree.maximum() == 70
    with pytest.raises(ValueError):
        BST().minimum()
    with pytest.raises(ValueError):
        BST().maximum()


def test_bst_traversals():
    tree = BST.build([5, 3, 2, 4, 8, 7, 9])
    assert tree.in_order() == [2, 3, 4, 5, 7, 8, 9]
    assert tree.pre_order() == [5, 3, 2, 4, 8, 7, 9]
    assert tree.post_order() == [2, 4, 3, 7, 9, 8, 5]
    assert tree.height() == 2


def test_bst_delete_leaf_and_single_child():
    tree = BST.build(VALUES)
    assert tree.delete(5)
    assert 5 not in tree
    assert tree.delete(65)
    assert 65 not in tree
    assert tree.in_order() == sorted(value for value in VALUES if value not in (5, 65))
    assert tree.is_valid()


def test_bst_delete_two_children_sequence():
    tree = BST.build(VALUES)
    assert tree.delete(35)
    assert 35 not in tree
    assert tree.is_valid()
    assert tree.delete(25)
    assert 25 not in tree
    assert tree.in_order() == sorted(value for value in VALUES if value not in (35, 25))
    assert tree.is_valid()


def test_bst_delete_missing_and_empty():
    tree = BST.build([2, 1, 3])
    assert not tree.delete(42)
    assert tree.delete(2)
    assert tree.in_order() == [1, 3]
    assert not tree.delete(2)
    assert BST().height() == -1
    assert BST().in_order() == []


def test_bst_size_and_eq():
    tree = BST.build([4, 2, 6])
    assert len(tree) == 3
    assert list(tree) == [2, 4, 6]
    assert repr(tree) == "BST([2, 4, 6])"


def test_render_tree():
    tree = BST.build([5, 3, 2, 4, 8, 7, 9])
    expected = "\n".join(
        [
            "5",
            "|-- 3",
            "|   |-- 2",
            "|   `-- 4",
            "`-- 8",
            "    |-- 7",
            "    `-- 9",
        ]
    )
    assert render_tree(tree.root) == expected
    assert tree_lines(None) == ["<empty>"]


def test_expression_tree_from_rpn():
    tree = build_from_rpn("3 4 +")
    assert evaluate(tree) == 7
    assert to_infix(tree) == "(3 + 4)"
    assert to_postfix(tree) == ["3", "4", "+"]
    assert height(tree) == 1


def test_expression_tree_with_variables():
    tree = build_from_rpn("5 z + -8 / 4 2 ^ *")
    assert to_infix(tree) == "((5 + z) / -8) * (4 ^ 2)" or to_infix(tree) == (
        "(((5 + z) / -8) * (4 ^ 2))"
    )
    assert evaluate(tree, {"z": 3}) == -16
    assert to_postfix(tree) == ["5", "z", "+", "-8", "/", "4", "2", "^", "*"]


def test_expression_tree_unary_minus():
    tree = build_from_rpn(["5", "z", "+", "8", "neg", "/", "4", "2", "^", "*"])
    assert to_infix(tree) == "(((5 + z) / (-8)) * (4 ^ 2))"
    assert evaluate(tree, {"z": 3}) == -16
    assert evaluate_rpn("5 z + 8 neg / 4 2 ^ *", {"z": 3}) == -16


def test_evaluate_rpn_matches_tree():
    tokens = ["1", "2", "+", "4", "*", "3", "+"]
    tree = build_from_rpn(tokens)
    assert evaluate(tree) == evaluate_rpn(tokens) == 15


@pytest.mark.parametrize(
    "expression",
    ["", "3 +", "3 4 + 5", "3 x @ +", "+ 3 4"],
)
def test_invalid_rpn(expression):
    with pytest.raises(ValueError):
        build_from_rpn(expression)


def test_unknown_variable():
    with pytest.raises(KeyError):
        evaluate(build_from_rpn("x 2 +"))
    with pytest.raises(KeyError):
        evaluate_rpn("x 2 +")


def test_ternary_simple():
    tree = parse_ternary("a?b:c")
    assert tree.value == "a"
    assert tree.left is not None and tree.left.value == "b"
    assert tree.right is not None and tree.right.value == "c"
    assert to_ternary(tree) == "a?b:c"
    assert to_ternary(tree, parenthesize=True) == "(a?b:c)"


def test_ternary_nested():
    tree = parse_ternary("a?b?c:d:e")
    assert tree.value == "a"
    assert tree.left is not None and tree.left.value == "b"
    assert tree.left.left is not None and tree.left.left.value == "c"
    assert tree.left.right is not None and tree.left.right.value == "d"
    assert tree.right is not None and tree.right.value == "e"
    assert to_ternary(tree) == "a?b?c:d:e"
    assert to_ternary(tree, parenthesize=True) == "(a?(b?c:d):e)"


def test_ternary_evaluation():
    tree = parse_ternary("a?b?c:d:e")
    assert evaluate_ternary(tree, {"a": True, "b": True}) == "c"
    assert evaluate_ternary(tree, {"a": True, "b": False}) == "d"
    assert evaluate_ternary(tree, {"a": False, "b": True}) == "e"


def test_ternary_whitespace():
    tree = parse_ternary("  a ? b : c  ")
    assert to_ternary(tree) == "a?b:c"


@pytest.mark.parametrize("expression", ["", "a?", "a?b", "a?b:", "a?b:c:d", "a b"])
def test_invalid_ternary(expression):
    with pytest.raises(ValueError):
        parse_ternary(expression)


def test_ternary_unknown_variable():
    with pytest.raises(KeyError):
        evaluate_ternary(parse_ternary("a?b:c"), {})


def _scripted(answers):
    iterator = iter(answers)

    def read(_prompt):
        return next(iterator)

    return read


def test_akinator_guesses_the_default_animal():
    output: list[str] = []
    game = Akinator()
    result = game.play(_scripted(["oui", "oui"]), output.append)
    assert result == "oiseau"
    assert "J'ai trouvé !" in output


def test_akinator_stops_when_no_animal():
    output: list[str] = []
    result = Akinator().play(_scripted(["non"]), output.append)
    assert result is None
    assert "à bientôt" in output[-1]


def test_akinator_learns_a_new_animal():
    output: list[str] = []
    game = Akinator()
    result = game.play(
        _scripted(["oui", "non", "chat", "A-t-il des moustaches ?", "oui"]),
        output.append,
    )
    assert result is None
    assert isinstance(game.root, AnimalNode)
    assert game.root.text == "A-t-il des moustaches ?"
    assert game.root.yes is not None and game.root.yes.text == "chat"
    assert game.root.no is not None and game.root.no.text == "oiseau"

    output.clear()
    result = game.play(_scripted(["oui", "oui", "oui"]), output.append)
    assert result == "chat"


def test_akinator_reasks_on_invalid_answer():
    output: list[str] = []
    result = Akinator().play(_scripted(["peut-être", "oui", "oui"]), output.append)
    assert result == "oiseau"
    assert "Répondez par o" in output[0]


def test_akinator_serialisation(tmp_path):
    game = Akinator()
    game.root = AnimalNode(
        "A-t-il des plumes ?", AnimalNode("oiseau"), AnimalNode("chien")
    )
    path = tmp_path / "akinator.json"
    game.save(path)
    loaded = Akinator.load(path)
    assert loaded.to_dict() == game.to_dict()
    assert loaded.play(_scripted(["oui", "oui", "oui"]), lambda _line: None) == "oiseau"
    assert loaded.clone().to_dict() == game.to_dict()


def test_akinator_invalid_json():
    with pytest.raises(ValueError):
        Akinator.from_dict({"text": "question", "yes": {"text": "a"}, "no": None})
