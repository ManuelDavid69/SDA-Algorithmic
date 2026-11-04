"""Démonstration du TP 5 : ABR, arbres d'expression, arbres ternaires et Akinator."""

from __future__ import annotations

from .akinator import Akinator
from .bst import BST
from .expression_tree import build_from_rpn, evaluate, to_infix, to_postfix
from .ternary import evaluate_ternary, parse_ternary, to_ternary
from .tree_printer import print_tree


def main() -> None:
    values = [25, 60, 35, 10, 5, 20, 65, 45, 70, 40, 50, 55, 30, 15]
    tree = BST.build(values)
    print("== Arbre binaire de recherche ==")
    print_tree(tree.root)
    print(f"parcours infixe : {tree.in_order()}")
    print(f"hauteur : {tree.height()}")
    tree.delete(35)
    tree.delete(25)
    print("\naprès suppression de 35 puis 25 :")
    print_tree(tree.root)

    print("\n== Arbre d'expression ==")
    expression = build_from_rpn("5 z + 8 neg / 4 2 ^ *")
    print(f"RPN : {to_postfix(expression)}")
    print(f"infixe : {to_infix(expression)}")
    print(f"valeur pour z = 3 : {evaluate(expression, {'z': 3})}")

    print("\n== Expression ternaire ==")
    ternary = parse_ternary("a?b?c:d:e")
    print(f"arbre : {to_ternary(ternary, parenthesize=True)}")
    for variables in (
        {"a": True, "b": True},
        {"a": True, "b": False},
        {"a": False, "b": True},
    ):
        print(f"{variables} -> {evaluate_ternary(ternary, variables)}")

    print("\n== Akinator ==")
    game = Akinator()
    first_answers = iter(["oui", "non", "chat", "A-t-il des moustaches ?", "oui"])
    second_answers = iter(["oui", "oui", "oui"])

    def ask(prompt: str) -> str:
        answer = next(first_answers, None)
        if answer is None:
            answer = next(second_answers, "")
        print(prompt, end="")
        print(answer)
        return answer

    print("première partie : le programme apprend un chat")
    game.play(ask, print)
    print("\ndeuxième partie : le programme devrait deviner le chat")
    game.play(ask, print)


if __name__ == "__main__":
    main()
