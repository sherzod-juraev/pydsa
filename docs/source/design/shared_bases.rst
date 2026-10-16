Shared Bases
============

Structures of the same kind implement their algorithms once. A concrete class supplies only
what makes it different.

.. code-block:: text

   BaseStructure
   ├── LinkedListBase ── SinglyList, DoublyList
   ├── Stack, Queue
   ├── HeapBase ──────── MinHeap, MaxHeap
   ├── BinaryTreeBase ── BinaryTree
   │   └── SearchTreeBase ── BSTree, AVLTree
   ├── Trie
   ├── HashTable
   └── Graph

Only ``BaseStructure`` is documented as part of the public API (see :doc:`../api/core`).
The family bases are implementation detail. Their methods are listed on each concrete class,
so a user never needs to look them up.

BaseStructure
-------------

Every structure reports its size with ``len()`` and can be emptied with ``clear()``. A
structure is falsy exactly when it holds no elements, so ``if structure:`` replaces an
``is_empty`` method. Operations that need an element call one shared check first, so every
structure raises :class:`~pydsa.exc.EmptyError` with the same message.

Linked lists
------------

``SinglyList`` and ``DoublyList`` differ only in how a node is linked. Search, counting,
removal by value, ``middle``, cycle detection, copying and ``reverse`` are written once
against a small node protocol. The subclass provides the link-specific primitives. This is
why the two lists have identical public methods.

Heaps
-----

``MinHeap`` and ``MaxHeap`` run the same sift-up and sift-down. The one thing that changes
is the answer to "may ``first`` sit above ``second``?". A subclass answers it with a single
comparison, so the two heaps are a few lines each.

Binary trees
------------

Traversals, ``height``, ``leaves`` and ``clear`` do not depend on how values are ordered, so
they live in the binary tree base. The search tree base adds ``search``, ``min_value``,
``max_value`` and ``in``, and leaves ``insert`` and ``remove`` to the subclass, because that
is exactly where :class:`~pydsa.trees.BSTree` and :class:`~pydsa.trees.AVLTree` differ.
