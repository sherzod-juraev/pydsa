Principles
==========

Built from scratch
------------------

Linked lists, trees, and the ``Stack``/``Queue`` adapters built on them manage their own
nodes and pointers, with no built-in ``list`` or ``dict`` underneath their core logic.

Heaps, ``Graph``, ``Trie``, and ``HashTable`` do use a Python ``list`` or ``dict`` as their
underlying array or mapping. That is the standard building block for those structures: an
array *is* how a heap is implemented, and a mapping *is* how adjacency lists and trie
children are represented. It is not a shortcut around the point of the library.

Zero dependencies
-----------------

pydsa has no runtime dependencies. A library whose whole point is showing the algorithm
itself gains nothing from delegating the work to a numerical package.

Clarity over performance
------------------------

Implementations favor being readable and correct over being fast. The goal is not to
outperform Python's built-in ``list``, ``dict`` or ``heapq``. It is to see how the structures
work by building them.

Typed and consistent
--------------------

The code uses the generics syntax of Python 3.12 (:pep:`695`) and passes ``mypy --strict``.
Structures behave the same way where they can: the same size and truthiness rules, the same
error for an empty structure, and the same exception hierarchy.
