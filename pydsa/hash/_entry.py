"""Entry type for hash table buckets.

Provides :class:`Entry`, an internal key-value pair used inside each
bucket of :class:`~pydsa.hash.hash_table.HashTable`. Not intended for
direct use outside :mod:`pydsa.hash`.
"""


class Entry[K, V]:
    """A single key-value pair stored in a hash table bucket.

    Parameters
    ----------
    key : K
        The key.
    value : V
        The value associated with the key.
    """

    def __init__(self, key: K, value: V) -> None:
        """Initialize an entry with the given key and value."""
        self.key: K = key
        self.value: V = value
