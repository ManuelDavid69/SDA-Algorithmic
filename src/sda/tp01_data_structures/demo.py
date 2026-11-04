"""Démonstration du TP 1 : liste chaînée, train et analyse de parenthèses."""

from .linked_list import LinkedList
from .stack import Stack, analyse_text
from .train import Train


def main() -> None:
    print("== Liste chaînée ==")
    numbers = LinkedList([3, 7, 11])
    print(numbers)
    numbers.insert(5, 1)
    numbers.append(13)
    print(f"après insert(5, 1) et append(13) : {numbers}")
    print(f"search(11) -> {numbers.search(11)}")
    print(f"delete(2) -> {numbers.delete(2)} ; liste : {numbers}")

    print("\n== Train ==")
    train = Train(wagons=3, capacity=4)
    print(train)
    for passenger in ("Alice", "Bob", "Chloe", "David", "Eve"):
        wagon = train.board(passenger, 1)
        print(f"{passenger} monte dans le wagon {wagon}")
    print(train)
    print(f"{train.alight(1)} descend du wagon 1")
    print(train)

    print("\n== Pile ==")
    stack = Stack()
    for token in ("a", "b", "c"):
        stack.push(token)
    print(stack)
    print(f"pop -> {stack.pop()}, peek -> {stack.peek()}")

    print("\n== Analyse de parenthèses ==")
    for expression in ("{[()]}", "([)]", "((a + b)", "a]b"):
        report = analyse_text(expression)
        status = "valide" if report else f"invalide : {report.message}"
        print(f"{expression!r}: {status}")


if __name__ == "__main__":
    main()
