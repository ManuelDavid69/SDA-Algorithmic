"""A simplified Akinator: a tree of questions and animals (TP 5, exercise 4)."""

from __future__ import annotations

import copy
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

YES = {"o", "oui", "y", "yes"}
NO = {"n", "non", "no"}


@dataclass
class AnimalNode:
    """A question (two children) or an animal name (a leaf)."""

    text: str
    yes: AnimalNode | None = None
    no: AnimalNode | None = None

    @property
    def is_leaf(self) -> bool:
        return self.yes is None and self.no is None


def default_tree() -> AnimalNode:
    return AnimalNode("oiseau")


@dataclass
class Akinator:
    """The guessing game.

    ``input_fn`` and ``output_fn`` are injectable so that the game can be
    tested without a real terminal.
    """

    root: AnimalNode = field(default_factory=default_tree)

    def play(
        self,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> str | None:
        if not self._ask_yes_no("Pensez-vous à un animal ?", input_fn, output_fn):
            output_fn("D'accord, à bientôt !")
            return None
        self.root, found = self._visit(self.root, input_fn, output_fn)
        return found

    def _visit(
        self,
        node: AnimalNode,
        input_fn: Callable[[str], str],
        output_fn: Callable[[str], None],
    ) -> tuple[AnimalNode, str | None]:
        if node.is_leaf:
            if self._ask_yes_no(f"Est-ce un {node.text} ?", input_fn, output_fn):
                output_fn("J'ai trouvé !")
                return node, node.text
            return self._learn(node, input_fn, output_fn), None

        if self._ask_yes_no(node.text, input_fn, output_fn):
            assert node.yes is not None
            node.yes, found = self._visit(node.yes, input_fn, output_fn)
        else:
            assert node.no is not None
            node.no, found = self._visit(node.no, input_fn, output_fn)
        return node, found

    def _learn(
        self,
        old_animal: AnimalNode,
        input_fn: Callable[[str], str],
        output_fn: Callable[[str], None],
    ) -> AnimalNode:
        name = self._ask_text("Quel est le nom de l'animal ?", input_fn)
        question = self._ask_text(
            f"Quelle question distinguerait un {name} d'un {old_animal.text} ?",
            input_fn,
        )
        answer_for_new = self._ask_yes_no(
            f"Si l'animal était un {name}, quelle serait la réponse à cette question ?",
            input_fn,
            output_fn,
        )
        new_animal = AnimalNode(name)
        if answer_for_new:
            tree = AnimalNode(question, new_animal, old_animal)
        else:
            tree = AnimalNode(question, old_animal, new_animal)
        output_fn("Je l'ai appris !")
        return tree

    @staticmethod
    def _ask_text(question: str, input_fn: Callable[[str], str]) -> str:
        while True:
            answer = input_fn(question + " ").strip()
            if answer:
                return answer

    @staticmethod
    def _ask_yes_no(
        question: str,
        input_fn: Callable[[str], str],
        output_fn: Callable[[str], None],
    ) -> bool:
        while True:
            answer = input_fn(question + " (o/n) ").strip().lower()
            if answer in YES:
                return True
            if answer in NO:
                return False
            output_fn("Répondez par o (oui) ou n (non).")

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        def convert(node: AnimalNode) -> dict:
            return {
                "text": node.text,
                "yes": convert(node.yes) if node.yes is not None else None,
                "no": convert(node.no) if node.no is not None else None,
            }

        return convert(self.root)

    @classmethod
    def from_dict(cls, data: dict) -> Akinator:
        def convert(payload: dict) -> AnimalNode:
            if not isinstance(payload, dict) or "text" not in payload:
                raise ValueError("invalid Akinator node")
            yes = convert(payload["yes"]) if payload.get("yes") is not None else None
            no = convert(payload["no"]) if payload.get("no") is not None else None
            if (yes is None) != (no is None):
                raise ValueError("a question must have exactly two children")
            return AnimalNode(str(payload["text"]), yes, no)

        return cls(root=convert(data))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @classmethod
    def load(cls, path: str | Path) -> Akinator:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def clone(self) -> Akinator:
        return Akinator(root=copy.deepcopy(self.root))
