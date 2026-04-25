"""Hash table with open addressing and linear probing (TP 6, exercise 1)."""

from __future__ import annotations

from typing import Any

EMPTY = object()
DELETED = object()


class HashTable:
    """A fixed-size hash table with linear probing and DELETED markers.

    The hash function of the statement is ``h(k) = k mod m``.  Deletions use a
    tombstone (``DELETED``) instead of resetting the slot to ``EMPTY``: a
    search must keep probing past a deleted slot, otherwise it could stop
    before reaching a key that was inserted after a collision.
    """

    def __init__(self, size: int = 1009, hash_function=None) -> None:
        if size < 1:
            raise ValueError("the table must contain at least one slot")
        self.capacity = size
        self._keys: list[Any] = [EMPTY] * size
        self._values: list[Any] = [None] * size
        self._size = 0
        self._occupied = 0  # slots that are not EMPTY (keys + tombstones)
        self._hash_function = hash_function or (lambda key: key % size)

    # ------------------------------------------------------------------
    # Basic properties
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: int) -> bool:
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def __repr__(self) -> str:
        return f"HashTable(size={self._size}, capacity={self.capacity})"

    @property
    def load_factor(self) -> float:
        """Number of stored elements divided by the capacity."""
        return self._size / self.capacity

    @property
    def occupied_ratio(self) -> float:
        """Slots that are not EMPTY, including tombstones."""
        return self._occupied / self.capacity

    def _index(self, key: int) -> int:
        if not isinstance(key, int):
            raise TypeError("this table only indexes integer keys")
        return self._hash_function(key) % self.capacity

    # ------------------------------------------------------------------
    # Insertion, search and deletion
    # ------------------------------------------------------------------
    def insert(self, key: int, value: Any) -> int:
        """Insert or update ``key``; return the number of extra probes.

        A probe is one slot examined after the home slot.  A return value of
        ``0`` therefore means that the key went directly into its home slot.
        """
        index = self._index(key)
        first_deleted: int | None = None
        for probes in range(self.capacity):
            slot = self._keys[index]
            if slot is EMPTY:
                target = first_deleted if first_deleted is not None else index
                if first_deleted is None:
                    self._occupied += 1
                self._keys[target] = key
                self._values[target] = value
                self._size += 1
                return probes
            if slot is DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif slot == key:
                self._values[index] = value
                return probes
            index = (index + 1) % self.capacity

        # No EMPTY slot was found: reuse a tombstone if possible.
        if first_deleted is not None:
            self._keys[first_deleted] = key
            self._values[first_deleted] = value
            self._size += 1
            return self.capacity
        raise OverflowError("the hash table is full")

    def _find_slot(self, key: int) -> int:
        index = self._index(key)
        for _ in range(self.capacity):
            slot = self._keys[index]
            if slot is EMPTY:
                raise KeyError(key)
            if slot is not DELETED and slot == key:
                return index
            index = (index + 1) % self.capacity
        raise KeyError(key)

    def get(self, key: int) -> Any:
        return self._values[self._find_slot(key)]

    def delete(self, key: int) -> Any:
        """Delete ``key`` and return its value; leave a DELETED tombstone."""
        index = self._find_slot(key)
        value = self._values[index]
        self._keys[index] = DELETED
        self._values[index] = None
        self._size -= 1
        return value

    def slot_of(self, key: int) -> int:
        """Index of the slot that contains ``key`` (mainly for tests)."""
        return self._find_slot(key)

    def keys(self) -> list[int]:
        return [key for key in self._keys if key is not EMPTY and key is not DELETED]

    def items(self) -> list[tuple[int, Any]]:
        return [
            (key, value)
            for key, value in zip(self._keys, self._values, strict=True)
            if key is not EMPTY and key is not DELETED
        ]
