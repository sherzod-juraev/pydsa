Hash Table
============

A hash table using separate chaining for collision resolution, with
a ``dict``-like interface (``table[key]``, ``key in table``,
``table.get(key, default)``) and automatic rehashing past a 0.75
load factor.

.. autoclass:: pydsa.HashTable
   :members:
