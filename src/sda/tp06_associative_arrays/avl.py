"""AVL tree indexed by year, with range queries (TP 6, exercise 2)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AVLNode:
    key: int
    refs: list[str] = field(default_factory=list)
    left: AVLNode | None = None
    right: AVLNode | None = None
    height: int = 1


class AVLTree:
    """An AVL tree whose nodes store a year and the catalogue references.

    Heights are counted in levels: an empty tree has height ``0`` and a leaf
    has height ``1``.  The balance factor of a node is
    ``height(left) - height(right)``.
    """

    def __init__(self) -> None:
        self.root: AVLNode | None = None
        self._size = 0
        self.rotations: list[str] = []

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"AVLTree({self.in_order()})"

    # ------------------------------------------------------------------
    # Rotations
    # ------------------------------------------------------------------
    @staticmethod
    def _height(node: AVLNode | None) -> int:
        return node.height if node is not None else 0

    @classmethod
    def _update_height(cls, node: AVLNode) -> None:
        node.height = 1 + max(cls._height(node.left), cls._height(node.right))

    @classmethod
    def _balance_factor(cls, node: AVLNode | None) -> int:
        if node is None:
            return 0
        return cls._height(node.left) - cls._height(node.right)

    @classmethod
    def _rotate_right(cls, node: AVLNode) -> AVLNode:
        assert node.left is not None
        pivot = node.left
        node.left = pivot.right
        pivot.right = node
        cls._update_height(node)
        cls._update_height(pivot)
        return pivot

    @classmethod
    def _rotate_left(cls, node: AVLNode) -> AVLNode:
        assert node.right is not None
        pivot = node.right
        node.right = pivot.left
        pivot.left = node
        cls._update_height(node)
        cls._update_height(pivot)
        return pivot

    # ------------------------------------------------------------------
    # Insertion
    # ------------------------------------------------------------------
    def insert(self, key: int, reference: str | None = None) -> None:
        """Insert ``key`` or append ``reference`` to an existing key."""
        self.root = self._insert(self.root, key, reference)

    def _insert(
        self, node: AVLNode | None, key: int, reference: str | None
    ) -> AVLNode:
        if node is None:
            self._size += 1
            return AVLNode(key, [reference] if reference is not None else [])

        if key < node.key:
            node.left = self._insert(node.left, key, reference)
        elif key > node.key:
            node.right = self._insert(node.right, key, reference)
        else:
            if reference is not None and reference not in node.refs:
                node.refs.append(reference)
            return node

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:
            assert node.left is not None
            if key < node.left.key:
                self.rotations.append("LL")
                return self._rotate_right(node)
            self.rotations.append("LR")
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            assert node.right is not None
            if key > node.right.key:
                self.rotations.append("RR")
                return self._rotate_left(node)
            self.rotations.append("RL")
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _find_node(self, node: AVLNode | None, key: int) -> AVLNode | None:
        while node is not None:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def search(self, key: int) -> list[str] | None:
        node = self._find_node(self.root, key)
        return list(node.refs) if node is not None else None

    # ------------------------------------------------------------------
    # Queries and traversal
    # ------------------------------------------------------------------
    def range_query(self, low: int, high: int) -> list[tuple[int, list[str]]]:
        """Return all ``(year, references)`` with ``low <= year <= high``.

        The traversal prunes subtrees that cannot intersect the interval, so
        the cost is ``O(log n + k)`` where ``k`` is the number of returned
        nodes.
        """
        if low > high:
            return []
        result: list[tuple[int, list[str]]] = []
        self._range(self.root, low, high, result)
        return result

    def _range(
        self,
        node: AVLNode | None,
        low: int,
        high: int,
        result: list[tuple[int, list[str]]],
    ) -> None:
        if node is None:
            return
        if node.key > low:
            self._range(node.left, low, high, result)
        if low <= node.key <= high:
            result.append((node.key, list(node.refs)))
        if node.key < high:
            self._range(node.right, low, high, result)

    def in_order(self) -> list[int]:
        result: list[int] = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node: AVLNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._in_order(node.left, result)
        result.append(node.key)
        self._in_order(node.right, result)

    def items(self) -> list[tuple[int, list[str]]]:
        result: list[tuple[int, list[str]]] = []
        self._items(self.root, result)
        return result

    def _items(self, node: AVLNode | None, result: list[tuple[int, list[str]]]) -> None:
        if node is None:
            return
        self._items(node.left, result)
        result.append((node.key, list(node.refs)))
        self._items(node.right, result)

    def height(self) -> int:
        return self._height(self.root)

    def balance_factors(self) -> dict[int, int]:
        factors: dict[int, int] = {}
        self._collect_factors(self.root, factors)
        return factors

    def _collect_factors(self, node: AVLNode | None, factors: dict[int, int]) -> None:
        if node is None:
            return
        factors[node.key] = self._balance_factor(node)
        self._collect_factors(node.left, factors)
        self._collect_factors(node.right, factors)

    def is_balanced(self) -> bool:
        return self._check_balanced(self.root)

    def _check_balanced(self, node: AVLNode | None) -> bool:
        if node is None:
            return True
        expected_height = 1 + max(self._height(node.left), self._height(node.right))
        if node.height != expected_height or abs(self._balance_factor(node)) > 1:
            return False
        return self._check_balanced(node.left) and self._check_balanced(node.right)
