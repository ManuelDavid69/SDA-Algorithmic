"""Table de hachage à adressage ouvert et sondage linéaire (TP 6, exercice 1)."""

from __future__ import annotations

from typing import Any

EMPTY = object()
DELETED = object()


class HashTable:
    """Une table de hachage de taille fixe avec sondage linéaire et marqueurs DELETED.

    La fonction de hachage de l'énoncé est ``h(k) = k mod m``. Les suppressions
    utilisent une pierre tombale (``DELETED``) au lieu de remettre l'emplacement
    à ``EMPTY`` : une recherche doit continuer à sonder au-delà d'un emplacement
    supprimé, sinon elle pourrait s'arrêter avant d'atteindre une clé insérée
    après une collision.
    """

    def __init__(self, size: int = 1009, hash_function=None) -> None:
        if size < 1:
            raise ValueError("la table doit contenir au moins un emplacement")
        self.capacity = size
        self._keys: list[Any] = [EMPTY] * size
        self._values: list[Any] = [None] * size
        self._size = 0
        self._occupied = 0  # emplacements qui ne sont pas EMPTY (clés + pierres tombales)
        self._hash_function = hash_function or (lambda key: key % size)

    # ------------------------------------------------------------------
    # Propriétés de base
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
        """Nombre d'éléments stockés divisé par la capacité."""
        return self._size / self.capacity

    @property
    def occupied_ratio(self) -> float:
        """Emplacements qui ne sont pas EMPTY, pierres tombales comprises."""
        return self._occupied / self.capacity

    def _index(self, key: int) -> int:
        if not isinstance(key, int):
            raise TypeError("cette table n'indexe que des clés entières")
        return self._hash_function(key) % self.capacity

    # ------------------------------------------------------------------
    # Insertion, recherche et suppression
    # ------------------------------------------------------------------
    def insert(self, key: int, value: Any) -> int:
        """Insère ou met à jour ``key`` ; renvoie le nombre de sondages supplémentaires.

        Un sondage correspond à un emplacement examiné après l'emplacement
        d'origine. Une valeur de retour de ``0`` signifie donc que la clé est
        allée directement dans son emplacement d'origine.
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

        # Aucun emplacement EMPTY trouvé : réutiliser une pierre tombale si possible.
        if first_deleted is not None:
            self._keys[first_deleted] = key
            self._values[first_deleted] = value
            self._size += 1
            return self.capacity
        raise OverflowError("la table de hachage est pleine")

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
        """Supprime ``key`` et renvoie sa valeur ; laisse une pierre tombale DELETED."""
        index = self._find_slot(key)
        value = self._values[index]
        self._keys[index] = DELETED
        self._values[index] = None
        self._size -= 1
        return value

    def slot_of(self, key: int) -> int:
        """Indice de l'emplacement qui contient ``key`` (principalement pour les tests)."""
        return self._find_slot(key)

    def keys(self) -> list[int]:
        return [key for key in self._keys if key is not EMPTY and key is not DELETED]

    def items(self) -> list[tuple[int, Any]]:
        return [
            (key, value)
            for key, value in zip(self._keys, self._values, strict=True)
            if key is not EMPTY and key is not DELETED
        ]
