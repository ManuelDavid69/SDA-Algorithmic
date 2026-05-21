"""Parser and evaluator for nested ternary expressions (TP 5, exercise 3).

Grammar (right-associative)::

    expression := atom ('?' expression ':' expression)?
    atom       := identifier
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass

_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")


@dataclass
class TernaryNode:
    """A ternary node: ``value ? left : right``."""

    value: str
    left: TernaryNode | None = None
    right: TernaryNode | None = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class _Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.position = 0

    def parse(self) -> TernaryNode:
        node = self._expression()
        self._skip_spaces()
        if self.position != len(self.text):
            raise ValueError(f"unexpected character at position {self.position}")
        return node

    def _expression(self) -> TernaryNode:
        condition = self._atom()
        self._skip_spaces()
        if self._peek() != "?":
            return condition
        self.position += 1
        when_true = self._expression()
        self._skip_spaces()
        if self._peek() != ":":
            raise ValueError(f"expected ':' at position {self.position}")
        self.position += 1
        when_false = self._expression()
        return TernaryNode(condition.value, when_true, when_false)

    def _atom(self) -> TernaryNode:
        self._skip_spaces()
        match = _IDENTIFIER.match(self.text, self.position)
        if match is None:
            raise ValueError(f"expected an identifier at position {self.position}")
        self.position = match.end()
        return TernaryNode(match.group())

    def _skip_spaces(self) -> None:
        while self.position < len(self.text) and self.text[self.position].isspace():
            self.position += 1

    def _peek(self) -> str:
        if self.position >= len(self.text):
            return ""
        return self.text[self.position]


def parse_ternary(text: str) -> TernaryNode:
    """Parse an expression such as ``a?b:c`` or ``a?b?c:d:e``."""
    if not text.strip():
        raise ValueError("empty expression")
    return _Parser(text).parse()


def evaluate_ternary(node: TernaryNode, variables: Mapping[str, bool]) -> bool | str:
    """Evaluate a ternary expression using a mapping of conditions."""
    if node.is_leaf:
        if node.value in variables:
            return variables[node.value]
        if node.value in ("true", "True"):
            return True
        if node.value in ("false", "False"):
            return False
        # A leaf can also be the result of the expression, e.g. the 'c' of
        # ``a?b:c``: in that case its name is the value of the expression.
        return node.value
    # The condition is an atom: resolve it directly.
    if node.value in variables:
        condition = variables[node.value]
    elif node.value in ("true", "True"):
        condition = True
    elif node.value in ("false", "False"):
        condition = False
    else:
        raise KeyError(f"unknown variable: {node.value!r}")
    branch = node.left if condition else node.right
    assert branch is not None
    return evaluate_ternary(branch, variables)


def to_ternary(node: TernaryNode, parenthesize: bool = False) -> str:
    """Reconstruct the expression; parentheses preserve the tree structure."""
    if node.is_leaf:
        return node.value
    assert node.left is not None and node.right is not None
    text = (
        f"{node.value}?{to_ternary(node.left, parenthesize)}:"
        f"{to_ternary(node.right, parenthesize)}"
    )
    return f"({text})" if parenthesize else text
