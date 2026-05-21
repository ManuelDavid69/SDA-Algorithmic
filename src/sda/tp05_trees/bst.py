"""Binary search tree with chained nodes (TP 5, exercise 1)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class BSTNode:
    key: int
    left: BSTNode | None = None
    right: BSTNode | None = None


class BST:
    """A binary search tree of integers.

    Every key is unique.  The three operations of the statement are
    ``insert``, ``search`` and ``delete``; the class also provides the three
    depth-first traversals and a validity check.
    """

    def __init__(self) -> None:
        self.root: BSTNode | None = None
        self._size = 0

    # ------------------------------------------------------------------
    # Size and representation
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self.root is not None

    def __contains__(self, key: int) -> bool:
        return self.search(key)

    def __iter__(self) -> Iterator[int]:
        return iter(self.in_order())

    def __repr__(self) -> str:
        return f"BST({self.in_order()})"

    @classmethod
    def build(cls, values) -> BST:
        tree = cls()
        for value in values:
            tree.insert(value)
        return tree

    # ------------------------------------------------------------------
    # Insertion and search
    # ------------------------------------------------------------------
    def insert(self, key: int) -> None:
        """Insert ``key``; duplicate keys are ignored."""
        if self.root is None:
            self.root = BSTNode(key)
            self._size = 1
            return
        if self._insert(self.root, key):
            self._size += 1

    def _insert(self, node: BSTNode, key: int) -> bool:
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
                return True
            return self._insert(node.left, key)
        if key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
                return True
            return self._insert(node.right, key)
        return False

    def find(self, key: int) -> BSTNode | None:
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def search(self, key: int) -> bool:
        return self.find(key) is not None

    # ------------------------------------------------------------------
    # Deletion
    # ------------------------------------------------------------------
    def delete(self, key: int) -> bool:
        """Delete ``key``; return ``True`` when it was present.

        Three cases: a leaf is removed, a node with one child is replaced by
        that child, and a node with two children is replaced by its in-order
        successor (the minimum of its right subtree).
        """
        self.root, removed = self._delete(self.root, key)
        if removed:
            self._size -= 1
        return removed

    def _delete(self, node: BSTNode | None, key: int) -> tuple[BSTNode | None, bool]:
        if node is None:
            return None, False
        if key < node.key:
            node.left, removed = self._delete(node.left, key)
            return node, removed
        if key > node.key:
            node.right, removed = self._delete(node.right, key)
            return node, removed

        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        successor = self._minimum_node(node.right)
        node.key = successor.key
        node.right, _ = self._delete(node.right, successor.key)
        return node, True

    def minimum(self) -> int:
        if self.root is None:
            raise ValueError("minimum of an empty tree")
        return self._minimum_node(self.root).key

    def maximum(self) -> int:
        if self.root is None:
            raise ValueError("maximum of an empty tree")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.key

    @staticmethod
    def _minimum_node(node: BSTNode) -> BSTNode:
        while node.left is not None:
            node = node.left
        return node

    # ------------------------------------------------------------------
    # Traversals and properties
    # ------------------------------------------------------------------
    def in_order(self) -> list[int]:
        result: list[int] = []
        _in_order(self.root, result)
        return result

    def pre_order(self) -> list[int]:
        result: list[int] = []
        _pre_order(self.root, result)
        return result

    def post_order(self) -> list[int]:
        result: list[int] = []
        _post_order(self.root, result)
        return result

    def height(self) -> int:
        """Height in edges: ``-1`` for an empty tree, ``0`` for a leaf."""
        return _height(self.root)

    def is_valid(self) -> bool:
        return _is_valid(self.root, None, None)


def _in_order(node: BSTNode | None, result: list[int]) -> None:
    if node is None:
        return
    _in_order(node.left, result)
    result.append(node.key)
    _in_order(node.right, result)


def _pre_order(node: BSTNode | None, result: list[int]) -> None:
    if node is None:
        return
    result.append(node.key)
    _pre_order(node.left, result)
    _pre_order(node.right, result)


def _post_order(node: BSTNode | None, result: list[int]) -> None:
    if node is None:
        return
    _post_order(node.left, result)
    _post_order(node.right, result)
    result.append(node.key)


def _height(node: BSTNode | None) -> int:
    if node is None:
        return -1
    return 1 + max(_height(node.left), _height(node.right))


def _is_valid(node: BSTNode | None, low: int | None, high: int | None) -> bool:
    if node is None:
        return True
    if low is not None and node.key <= low:
        return False
    if high is not None and node.key >= high:
        return False
    return _is_valid(node.left, low, node.key) and _is_valid(node.right, node.key, high)
