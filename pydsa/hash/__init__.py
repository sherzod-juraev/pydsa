"""Hash table package.

Exposes :class:`~pydsa.hash.hash_table.HashTable` as the public entry
point for this subpackage, a hash table with separate chaining for
collision resolution.
"""

from .hash_table import HashTable

__all__ = [
    "HashTable",
]
