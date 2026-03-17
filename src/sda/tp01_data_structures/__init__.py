"""Practical work 1: linked lists, stacks and bracket analysis."""

from .linked_list import LinkedList, Node
from .stack import BracketReport, Stack, analyse, analyse_file, analyse_text
from .train import Train, Wagon

__all__ = [
    "BracketReport",
    "LinkedList",
    "Node",
    "Stack",
    "Train",
    "Wagon",
    "analyse",
    "analyse_file",
    "analyse_text",
]
