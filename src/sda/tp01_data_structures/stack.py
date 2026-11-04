"""Pile chaînée et analyse de parenthèses (TP 1, exercice 2).

L'algorithme parcourt l'expression de gauche à droite :

* une parenthèse ouvrante est empilée ;
* une parenthèse fermante doit correspondre à la parenthèse au sommet de la
  pile, sinon l'expression est invalide ;
* à la fin, la pile doit être vide.

Seules les quatre paires de parenthèses utilisées dans le cours sont prises en
compte (``{}``, ``<>``, ``()`` et ``[]``) ; tout autre caractère est ignoré.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .linked_list import Node

OPENING = {"(": ")", "[": "]", "{": "}", "<": ">"}
CLOSING = {closing: opening for opening, closing in OPENING.items()}


class Stack:
    """Une pile LIFO implémentée à l'aide d'une liste simplement chaînée."""

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
            raise IndexError("dépilement d'une pile vide")
        node = self._head
        self._head = node.next
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if self._head is None:
            raise IndexError("consultation du sommet d'une pile vide")
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
    """Résultat de :func:`analyse_text`.

    ``line`` et ``column`` sont indexés à partir de 1 et désignent le premier
    caractère fautif.  Pour une parenthèse ouvrante non fermée, ils désignent
    cette parenthèse ouvrante.
    """

    valid: bool
    line: int | None = None
    column: int | None = None
    character: str | None = None
    message: str = ""

    def __bool__(self) -> bool:
        return self.valid


def analyse(expression: str) -> bool:
    """Renvoie ``True`` lorsque ``expression`` est correctement parenthésée."""
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
    """Analyse ``text`` et localise la première erreur de parenthésage, s'il y en a une."""
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
                    False, line, column, character, f"parenthèse fermante inattendue {character!r}"
                )
            opening, open_line, open_column = stack.peek()
            if opening != CLOSING[character]:
                return BracketReport(
                    False,
                    line,
                    column,
                    character,
                    f"{character!r} ferme {opening!r} ouvert à la ligne {open_line}, "
                    f"colonne {open_column}",
                )
            stack.pop()

    if not stack.is_empty():
        opening, open_line, open_column = stack.peek()
        return BracketReport(
            False,
            open_line,
            open_column,
            opening,
            f"parenthèse non fermée {opening!r}",
        )
    return BracketReport(True)


def analyse_file(path: str | Path) -> BracketReport:
    """Analyse un fichier texte UTF-8 et signale la première erreur de parenthésage."""
    text = Path(path).read_text(encoding="utf-8")
    return analyse_text(text)
