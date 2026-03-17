"""Linked stack and bracket analysis (TP 1, exercise 2).

The algorithm scans the expression from left to right:

* an opening bracket is pushed on the stack;
* a closing bracket must match the bracket on top of the stack, otherwise the
  expression is invalid;
* at the end, the stack must be empty.

Only the four bracket pairs used in the course are considered
(``{}``, ``<>``, ``()`` and ``[]``); every other character is ignored.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .linked_list import Node

OPENING = {"(": ")", "[": "]", "{": "}", "<": ">"}
CLOSING = {closing: opening for opening, closing in OPENING.items()}


class Stack:
    """A LIFO stack implemented with a singly linked list."""

    def __init__(self) -> None:
        self._head: Node | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return not self.is_empty()

    def is_empty(self) -> bool:
        return self._head is None

    @property
    def size(self) -> int:
        return self._size

    def push(self, value: Any) -> None:
        self._head = Node(value, self._head)
        self._size += 1

    def pop(self) -> Any:
        if self._head is None:
            raise IndexError("pop from an empty stack")
        node = self._head
        self._head = node.next
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if self._head is None:
            raise IndexError("peek at an empty stack")
        return self._head.value

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        return f"Stack({list(self)})"


@dataclass(frozen=True)
class BracketReport:
    """Result of :func:`analyse_text`.

    ``line`` and ``column`` are 1-based and point at the first faulty
    character.  For an unclosed opening bracket, they point at that opening
    bracket.
    """

    valid: bool
    line: int | None = None
    column: int | None = None
    character: str | None = None
    message: str = ""

    def __bool__(self) -> bool:
        return self.valid


def analyse(expression: str) -> bool:
    """Return ``True`` when ``expression`` is correctly parenthesised."""
    stack: Stack = Stack()
    for character in expression:
        if character in OPENING:
            stack.push(character)
        elif character in CLOSING:
            if stack.is_empty() or stack.peek() != CLOSING[character]:
                return False
            stack.pop()
    return stack.is_empty()


def analyse_text(text: str) -> BracketReport:
    """Analyse ``text`` and locate the first bracket error, if any."""
    stack: Stack = Stack()
    line = 1
    column = 0
    for character in text:
        if character == "\n":
            line += 1
            column = 0
            continue
        column += 1
        if character in OPENING:
            stack.push((character, line, column))
        elif character in CLOSING:
            if stack.is_empty():
                return BracketReport(
                    False, line, column, character, f"unexpected closing bracket {character!r}"
                )
            opening, open_line, open_column = stack.peek()
            if opening != CLOSING[character]:
                return BracketReport(
                    False,
                    line,
                    column,
                    character,
                    f"{character!r} closes {opening!r} opened at line {open_line}, "
                    f"column {open_column}",
                )
            stack.pop()

    if not stack.is_empty():
        opening, open_line, open_column = stack.peek()
        return BracketReport(
            False,
            open_line,
            open_column,
            opening,
            f"unclosed bracket {opening!r}",
        )
    return BracketReport(True)


def analyse_file(path: str | Path) -> BracketReport:
    """Analyse a UTF-8 text file and report the first bracket error."""
    text = Path(path).read_text(encoding="utf-8")
    return analyse_text(text)
