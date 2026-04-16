"""Practical work 5: binary search trees, expression trees, Akinator."""

from .bst import BST, BSTNode
from .expression_tree import (
    ExprNode,
    build_from_rpn,
    evaluate,
    evaluate_rpn,
    to_infix,
    to_postfix,
)
from .ternary import TernaryNode, evaluate_ternary, parse_ternary, to_ternary
from .tree_printer import print_tree, render_tree, tree_lines

__all__ = [
    "BST",
    "BSTNode",
    "ExprNode",
    "TernaryNode",
    "build_from_rpn",
    "evaluate",
    "evaluate_rpn",
    "evaluate_ternary",
    "parse_ternary",
    "print_tree",
    "render_tree",
    "to_infix",
    "to_postfix",
    "to_ternary",
    "tree_lines",
]
