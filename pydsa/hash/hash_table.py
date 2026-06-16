from collections.abc import Iterator
from typing import Any, TypeVar

from ..linear import SinglyList
from ._entry import Entry

K = TypeVar("K")
V = TypeVar("V")


class HashTable[K, V]:
    """
    A hash table with separate chaining for collision resolution.

    Keys are hashed to an index using Python's built-in ``hash()``
    modulo the table capacity. Each bucket stores entries in a
    ``SinglyList``, allowing multiple key-value pairs at the same
    index. When the load factor exceeds 0.75, the table automatically
    rehashes into double the capacity to maintain O(1) average
    performance.

    .. csv-table:: Time Complexity
       :header: "Operation", "Average", "Worst Case"
       :widths: 25, 15, 15

       "__getitem__", "O(1)", "O(n)"
       "__setitem__", "O(1)", "O(n)"
       "__delitem__", "O(1)", "O(n)"
       "__contains__", "O(1)", "O(n)"
       "get", "O(1)", "O(1)"
       "keys/values/items", "O(n)", "O(n)"
       "__len__", "O(1)", "O(1)"
       "clear", "O(m)", "O(m)"
       "__rehash", "O(n)", "O(n)"

    *n = number of entries, m = capacity*

    Notes
    -----
    - Uses separate chaining with ``SinglyList`` for each bucket.
    - Load factor threshold is 0.75; rehashing doubles capacity.
    - ``hash()`` is Python's built-in, capable of hashing any
      immutable object (str, int, float, tuple, etc.).
    - For open addressing variant, see ``HashTableOA`` (planned).
    - API mirrors Python's ``dict``: ``table[key]``, ``key in table``,
      ``del table[key]``, ``table.get(key, default)``.
    """
    def __init__(self, capacity: int) -> None:

        self.__capacity: int = capacity
        self.__data: list[SinglyList[Entry[K, V]]] = [SinglyList() for _ in range(capacity)]
        self.__size: int = 0

    def __len__(self) -> int:
        """Return the number of key-value pairs. O(1)."""
        return self.__size

    def __bool__(self) -> bool:
        """Return True if the table is not empty. O(1)."""
        return self.__size > 0

    def __getitem__(self, key: K) -> V:
        """Return the value for the given key. O(1) average.

        Raises
        ------
        KeyError
            If the key is not found.

        Examples
        --------
        >>> ht = HashTable()
        >>> ht["name"] = "John"
        >>> ht["name"]
        'John'
        """
        index = self.__hash(key)
        for entry in self.__data[index]:
            if entry.key == key:
                return entry.value
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key: K, value: V) -> None:
        """Insert or update a key-value pair. O(1) average.

        Triggers automatic rehashing if the load factor exceeds 0.75.

        Examples
        --------
        >>> ht = HashTable()
        >>> ht["age"] = 25
        >>> ht["age"] = 26  # update
        """
        index = self.__hash(key)
        for entry in self.__data[index]:
            if entry.key == key:
                entry.value = value
                return
        entry = Entry(key, value)
        self.__data[index].insert_last(entry)
        self.__size += 1
        if self.check_load():
            self.__rehash()

    def __delitem__(self, key: K) -> None:
        """Remove a key-value pair. O(1) average.

        Raises
        ------
        KeyError
            If the key is not found.

        Examples
        --------
        >>> del ht["age"]
        """
        index = self.__hash(key)
        for i, entry in enumerate(self.__data[index]):
            if entry.key == key:
                self.__data[index].remove_at(i)
                self.__size -= 1
                return
        raise KeyError(f"Key {key} not found")

    def remove(self, key: K, /) -> bool:
        """Remove a key-value pair if it exists. O(1) average.

        Returns True if the key was found and removed, False otherwise.
        """
        index = self.__hash(key)
        for i, entry in enumerate(self.__data[index]):
            if entry.key == key:
                self.__data[index].remove_at(i)
                self.__size -= 1
                return True
        return False

    def __contains__(self, item: K) -> bool:
        """Return True if the key exists. O(1) average.

        Examples
        --------
        >>> "name" in ht
        True
        """
        index = self.__hash(item)
        return any(entry.key == item for entry in self.__data[index])

    def get(self, key: K, default: V | None = None) -> Any:
        """Return the value for the key, or a default if missing. O(1).

        Parameters
        ----------
        key : Any
            The key to look up.
        default : Any, optional
            Value returned when the key is not found (default None).

        Returns
        -------
        Any
            The associated value or the default.

        Examples
        --------
        >>> ht.get("missing", 0)
        0
        """
        index = self.__hash(key)
        for entry in self.__data[index]:
            if entry.key == key:
                return entry.value
        return default

    def keys(self) -> Iterator[K]:
        """Yield all keys in the table. O(n)."""
        for bucket in self.__data:
            if bucket.is_empty():
                continue
            for entry in bucket:
                yield entry.key

    def values(self) -> Iterator[V]:
        """Yield all values in the table. O(n)."""
        for bucket in self.__data:
            if bucket.is_empty():
                continue
            for entry in bucket:
                yield entry.value

    def items(self) -> Iterator[tuple[K, V]]:
        """Yield all (key, value) pairs in the table. O(n)."""
        for i in range(len(self.__data)):
            if self.__data[i].is_empty():
                continue
            for entry in self.__data[i]:
                yield (entry.key, entry.value)

    def clear(self) -> None:
        """Remove all key-value pairs. O(m)."""
        self.__data = [SinglyList() for _ in range(self.__capacity)]
        self.__size = 0

    def __hash(self, key: K, /) -> int:
        """Compute the bucket index for a key."""
        return hash(key) % self.__capacity

    def __rehash(self) -> None:
        """Double the capacity and redistribute all entries. O(n)."""
        old_data = self.__data
        self.__capacity *= 2
        self.clear()
        for bucket in old_data:
            for entry in bucket:
                self[entry.key] = entry.value

    def check_load(self) -> bool:
        """Return True if the load factor exceeds 0.75."""
        return self.__size / self.__capacity > 0.75
