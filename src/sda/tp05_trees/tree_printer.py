"""ASCII rendering of binary trees (TP 5, exercise 1, question 3)."""

from __future__ import annotations

from collections.abc import Callable

from .bst import BSTNode


def tree_lines(node: BSTNode | None) -> list[str]:
    """Return an ASCII representation of the tree, one line per node."""
    if node is None:
        return ["<empty>"]
    lines = [str(node.key)]
    children = [child for child in (node.left, node.right) if child is not None]
    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        lines.extend(_render(child, "", is_last))
    return lines


def _render(node: BSTNode, prefix: str, is_last: bool) -> list[str]:
    connector = "`-- " if is_last else "|-- "
    lines = [prefix + connector + str(node.key)]
    child_prefix = prefix + ("    " if is_last else "|   ")
    children = [child for child in (node.left, node.right) if child is not None]
    for index, child in enumerate(children):
        lines.extend(_render(child, child_prefix, index == len(children) - 1))
    return lines


def render_tree(node: BSTNode | None) -> str:
    return "\n".join(tree_lines(node))


def print_tree(node: BSTNode | None, output: Callable[[str], None] = print) -> None:
    output(render_tree(node))
