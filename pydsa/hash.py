"""Hash table with separate chaining.

Provides :class:`HashTable`, a dict-like mapping that resolves collisions with
one :class:`~pydsa.linear.SinglyList` per bucket and doubles its capacity when
the load factor passes 0.75.
"""

from collections.abc import Iterator

from .core import BaseStructure
from .exc import InvalidValueError, KeyNotFoundError
from .linear import SinglyList


class _Entry[K, V]:
    """A mutable key-value pair stored in a :class:`HashTable` bucket.

    Attributes
    ----------
    key : K
        The key. It is never reassigned after the entry is created.
    value : V
        The value. It is replaced in place when the key is set again.
    """

    def __init__(self, key: K, value: V) -> None:
        """Create an entry holding ``key`` and ``value``."""
        self.key: K = key
        self.value: V = value


class HashTable[K, V](BaseStructure):
    """A hash table with separate chaining for collision resolution.

    A key is mapped to a bucket with ``hash(key) % capacity``. Each bucket is a
    :class:`~pydsa.linear.SinglyList` of entries, so several keys can share a
    bucket. After every insertion of a new key the load factor ``size / capacity``
    is checked; once it is strictly greater than ``0.75`` the table doubles its
    capacity and redistributes every entry.

    Time Complexity Summary

    .. csv-table:: Hash Table Operations Complexity
       :header: "Operation", "Average", "Worst Case"
       :widths: 25, 15, 15

       "__getitem__", "O(1)", "O(n)"
       "__setitem__", "O(1) amortized", "O(n)"
       "__delitem__", "O(1)", "O(n)"
       "remove", "O(1)", "O(n)"
       "__contains__", "O(1)", "O(n)"
       "get", "O(1)", "O(n)"
       "keys/values/items", "O(m + n)", "O(m + n)"
       "__len__", "O(1)", "O(1)"
       "clear", "O(m)", "O(m)"

    *n = number of entries, m = number of buckets.*

    Notes
    -----
    - Keys must be hashable; an unhashable key raises ``TypeError``, as with ``dict``.
    - Keys that are equal and have equal hashes are the same key
      (``1``, ``1.0`` and ``True`` share one entry).
    - Iteration follows bucket order, not insertion order, and the order changes
      after a rehash. Do not modify the table while iterating over it.
    - An empty table is falsy and a non-empty one is truthy.

    Examples
    --------
    >>> table = HashTable[str, int](capacity=8)
    >>> table["apple"] = 3
    >>> table["pear"] = 5
    >>> table["apple"]
    3
    >>> len(table)
    2
    >>> "pear" in table
    True
    >>> del table["pear"]
    >>> table.get("pear", 0)
    0
    """

    _LOAD_FACTOR: float = 0.75

    def __init__(self, capacity: int) -> None:
        """Create an empty table with ``capacity`` buckets.

        Parameters
        ----------
        capacity : int
            Initial number of buckets. The table grows on its own, so this is only a
            starting size.

        Raises
        ------
        InvalidValueError
            If ``capacity`` is not a positive integer.
        """
        if capacity <= 0:
            raise InvalidValueError(f"Capacity must be a positive integer, got {capacity!r}")
        self.__capacity: int = capacity
        self.__data: list[SinglyList[_Entry[K, V]]] = [SinglyList() for _ in range(capacity)]
        self.__size: int = 0

    def __len__(self) -> int:
        """Return the number of key-value pairs. O(1)."""
        return self.__size

    def __getitem__(self, key: K) -> V:
        """Return the value stored under ``key``. O(1) average, O(n) worst case.

        Parameters
        ----------
        key : K
            The key to look up.

        Returns
        -------
        V
            The value associated with ``key``.

        Raises
        ------
        KeyNotFoundError
            If ``key`` is not in the table.

        Examples
        --------
        >>> table = HashTable[str, str](capacity=8)
        >>> table["name"] = "Ada"
        >>> table["name"]
        'Ada'
        """
        index = self._index(key)
        for entry in self.__data[index]:
            if entry.key == key:
                return entry.value
        raise KeyNotFoundError(f"Key {key!r} not found")

    def __setitem__(self, key: K, value: V) -> None:
        """Store ``value`` under ``key``, replacing any previous value.

        O(1) amortized on average, O(n) worst case. Adding a new key may trigger a
        rehash, which costs O(n) for that single call. Updating an existing key never
        changes the size of the table.

        Parameters
        ----------
        key : K
            The key to store.
        value : V
            The value to associate with ``key``.

        Examples
        --------
        >>> table = HashTable[str, int](capacity=8)
        >>> table["a"] = 1
        >>> table["a"] = 2
        >>> table["a"], len(table)
        (2, 1)
        """
        index = self._index(key)
        for entry in self.__data[index]:
            if entry.key == key:
                entry.value = value
                return
        entry = _Entry(key, value)
        self.__data[index].insert_last(entry)
        self.__size += 1
        if self._needs_rehash():
            self.__rehash()

    def __delitem__(self, key: K) -> None:
        """Delete ``key`` and its value. O(1) average, O(n) worst case.

        Parameters
        ----------
        key : K
            The key to delete.

        Raises
        ------
        KeyNotFoundError
            If ``key`` is not in the table.

        Examples
        --------
        >>> table = HashTable[str, int](capacity=8)
        >>> table["a"] = 1
        >>> del table["a"]
        >>> "a" in table
        False
        """
        if not self.remove(key):
            raise KeyNotFoundError(f"Key {key!r} not found")

    def remove(self, key: K, /) -> bool:
        """Delete ``key`` if present and report whether it was.

        Unlike ``del table[key]`` this never raises for a missing key.
        O(1) average, O(n) worst case.

        Parameters
        ----------
        key : K
            The key to delete.

        Returns
        -------
        bool
            ``True`` if the key was found and deleted, ``False`` otherwise.

        Examples
        --------
        >>> table = HashTable[str, int](capacity=8)
        >>> table["a"] = 1
        >>> table.remove("a")
        True
        >>> table.remove("a")
        False
        """
        index = self._index(key)
        for i, entry in enumerate(self.__data[index]):
            if entry.key == key:
                self.__data[index].remove_at(i)
                self.__size -= 1
                return True
        return False

    def __contains__(self, item: K) -> bool:
        """Return ``True`` if ``item`` is a key of the table. O(1) average, O(n) worst case.

        Only keys are tested, never values.

        Examples
        --------
        >>> table = HashTable[str, int](capacity=8)
        >>> table["a"] = 1
        >>> "a" in table, 1 in table
        (True, False)
        """
        index = self._index(item)
        return any(entry.key == item for entry in self.__data[index])

    def get(self, key: K, default: V | None = None) -> V | None:
        """Return the value for ``key``, or ``default`` if the key is missing.

        O(1) average, O(n) worst case. The default is returned as is and is never
        stored in the table.

        Parameters
        ----------
        key : K
            The key to look up.
        default : V or None, optional
            Value returned when ``key`` is missing. Defaults to ``None``.

        Returns
        -------
        V or None
            The stored value, or ``default``. A stored ``None`` is returned as
            ``None``, not replaced by ``default``.

        Examples
        --------
        >>> table = HashTable[str, int](capacity=8)
        >>> table["a"] = 1
        >>> table.get("a"), table.get("b"), table.get("b", 0)
        (1, None, 0)
        """
        index = self._index(key)
        for entry in self.__data[index]:
            if entry.key == key:
                return entry.value
        return default

    def keys(self) -> Iterator[K]:
        """Iterate over the keys in bucket order. O(m + n).

        Yields
        ------
        K
            Each key exactly once. The order is unspecified.

        Examples
        --------
        >>> table = HashTable[int, str](capacity=8)
        >>> table[1], table[2] = "one", "two"
        >>> sorted(table.keys())
        [1, 2]
        """
        for bucket in self.__data:
            for entry in bucket:
                yield entry.key

    def values(self) -> Iterator[V]:
        """Iterate over the values in bucket order. O(m + n).

        Yields
        ------
        V
            The value of each entry. The order matches :meth:`keys`.

        Examples
        --------
        >>> table = HashTable[int, str](capacity=8)
        >>> table[1], table[2] = "one", "two"
        >>> sorted(table.values())
        ['one', 'two']
        """
        for bucket in self.__data:
            for entry in bucket:
                yield entry.value

    def items(self) -> Iterator[tuple[K, V]]:
        """Iterate over ``(key, value)`` pairs in bucket order. O(m + n).

        Yields
        ------
        tuple of (K, V)
            Each entry exactly once. The order matches :meth:`keys`.

        Examples
        --------
        >>> table = HashTable[int, str](capacity=8)
        >>> table[1], table[2] = "one", "two"
        >>> sorted(table.items())
        [(1, 'one'), (2, 'two')]
        """
        for bucket in self.__data:
            for entry in bucket:
                yield (entry.key, entry.value)

    def clear(self) -> None:
        """Remove every key-value pair. O(m).

        The table is empty and usable afterwards.

        Examples
        --------
        >>> table = HashTable[str, int](capacity=8)
        >>> table["a"] = 1
        >>> table.clear()
        >>> len(table), "a" in table
        (0, False)
        """
        self._reset()

    def _reset(self) -> None:
        """Replace all buckets with empty ones at the current capacity and set the size to zero."""
        self.__data = [SinglyList() for _ in range(self.__capacity)]
        self.__size = 0

    def _index(self, key: K, /) -> int:
        """Return the index of the bucket that ``key`` belongs to."""
        return hash(key) % self.__capacity

    def _needs_rehash(self) -> bool:
        """Return ``True`` if the load factor is strictly above the threshold."""
        return self.__size / self.__capacity > self._LOAD_FACTOR

    def __rehash(self) -> None:
        """Double the capacity and redistribute every entry. O(n)."""
        old_data = self.__data
        self.__capacity *= 2
        self._reset()
        for bucket in old_data:
            for entry in bucket:
                self._set_raw(entry.key, entry.value)

    def _set_raw(self, key: K, value: V) -> None:
        """Insert or update ``key`` without checking the load factor.

        Used while redistributing entries, where the capacity has just been enlarged and
        a nested rehash must not start.
        """
        index = self._index(key)
        for entry in self.__data[index]:
            if entry.key == key:
                entry.value = value
                return
        entry = _Entry(key, value)
        self.__data[index].insert_last(entry)
        self.__size += 1
