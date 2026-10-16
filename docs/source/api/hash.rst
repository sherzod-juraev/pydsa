Hash Table
==========

A hash table using separate chaining for collision resolution, with a ``dict``-like
interface (``table[key]``, ``key in table``, ``table.get(key, default)``) and automatic
rehashing once the load factor passes 0.75. Each bucket is a
:class:`~pydsa.linear.SinglyList`.

.. autoclass:: pydsa.hash.HashTable
   :members:
