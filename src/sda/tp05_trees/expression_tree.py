"""Expression trees and reverse Polish notation (TP 5, exercise 2)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping, Sequence

BINARY_OPERATORS = {"+", "-", "*", "/", "^"}
UNARY_MINUS = "neg"
_NUMBER = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")
_IDENTIFIER = re.compile(r"^[A-Za-z_]\w*$")


@dataclass
class ExprNode:
    """A node of an expression tree.

    Leaves contain an operand (number or variable); internal nodes contain an
    operator.  ``neg`` is the unary minus operator, with only a left child.
    """

    value: str
    left: ExprNode | None = None
    right: ExprNode | None = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_from_rpn(expression: str | Sequence[str]) -> ExprNode:
    """Build an expression tree from a postfix (RPN) expression."""
    tokens = expression.split() if isinstance(expression, str) else list(expression)
    if not tokens:
        raise ValueError("empty expression")
    stack: list[ExprNode] = []
    for token in tokens:
        if token in BINARY_OPERATORS:
            if len(stack) < 2:
                raise ValueError(f"not enough operands for {token!r}")
            right = stack.pop()
            left = stack.pop()
            stack.append(ExprNode(token, left, right))
        elif token == UNARY_MINUS:
            if not stack:
                raise ValueError("not enough operands for unary minus")
            stack.append(ExprNode(UNARY_MINUS, stack.pop()))
        elif _NUMBER.match(token) or _IDENTIFIER.match(token):
            stack.append(ExprNode(token))
        else:
            raise ValueError(f"invalid token: {token!r}")
    if len(stack) != 1:
        raise ValueError("the expression has leftover operands")
    return stack[0]


def evaluate(node: ExprNode, variables: Mapping[str, float] | None = None) -> float | int:
    """Evaluate an expression tree; variables are looked up in ``variables``."""
    variables = variables or {}
    if node.is_leaf:
        if _NUMBER.match(node.value):
            number = float(node.value)
            return int(number) if number.is_integer() and "." not in node.value else number
        try:
            return variables[node.value]
        except KeyError as error:
            raise KeyError(f"unknown variable: {node.value!r}") from error
    if node.value == UNARY_MINUS:
        assert node.left is not None
        return -evaluate(node.left, variables)
    assert node.left is not None and node.right is not None
    left = evaluate(node.left, variables)
    right = evaluate(node.right, variables)
    if node.value == "+":
        return left + right
    if node.value == "-":
        return left - right
    if node.value == "*":
        return left * right
    if node.value == "/":
        return left / right
    if node.value == "^":
        return left**right
    raise ValueError(f"unknown operator: {node.value!r}")


def to_infix(node: ExprNode) -> str:
    """Infix traversal with the parentheses needed to keep the structure."""
    if node.is_leaf:
        return node.value
    if node.value == UNARY_MINUS:
        assert node.left is not None
        return f"(-{to_infix(node.left)})"
    assert node.left is not None and node.right is not None
    return f"({to_infix(node.left)} {node.value} {to_infix(node.right)})"


def to_postfix(node: ExprNode) -> list[str]:
    """Post-order traversal: the RPN form of the expression."""
    if node.is_leaf:
        return [node.value]
    if node.value == UNARY_MINUS:
        assert node.left is not None
        return to_postfix(node.left) + [UNARY_MINUS]
    assert node.left is not None and node.right is not None
    return to_postfix(node.left) + to_postfix(node.right) + [node.value]


def height(node: ExprNode | None) -> int:
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


def evaluate_rpn(expression: str | Sequence[str], variables: Mapping[str, float] | None = None):
    """Evaluate an RPN expression directly with a stack (no tree needed)."""
    tokens = expression.split() if isinstance(expression, str) else list(expression)
    variables = variables or {}
    stack: list[float] = []
    for token in tokens:
        if token in BINARY_OPERATORS:
            if len(stack) < 2:
                raise ValueError(f"not enough operands for {token!r}")
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            elif token == "/":
                stack.append(left / right)
            else:
                stack.append(left**right)
        elif token == UNARY_MINUS:
            if not stack:
                raise ValueError("not enough operands for unary minus")
            stack.append(-stack.pop())
        elif _NUMBER.match(token):
            stack.append(float(token))
        elif _IDENTIFIER.match(token):
            if token not in variables:
                raise KeyError(f"unknown variable: {token!r}")
            stack.append(variables[token])
        else:
            raise ValueError(f"invalid token: {token!r}")
    if len(stack) != 1:
        raise ValueError("the expression has leftover operands")
    return stack[0]
