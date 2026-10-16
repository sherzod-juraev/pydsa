Changelog
=========

2.0.0
-----

A restructuring release. The package was reorganised around shared base classes and a single
exception hierarchy. Several changes are **breaking**.

Breaking changes
~~~~~~~~~~~~~~~~

- **Imports.** Structures and functions are no longer re-exported from the top-level
  package. Import them from their submodule.
- **No** ``is_empty``. Use truthiness: ``if structure:`` or ``len(structure) == 0``.
- **Linked list** ``remove(value)`` returns ``True`` or ``False`` and never raises, for a
  missing value or for an empty list.
- **BinaryTree.insert** places a value only in an empty slot. An empty path is allowed
  only on an empty tree. A malformed path, a missing intermediate node or an occupied slot
  raises :class:`~pydsa.exc.InvalidPathError` and leaves the tree unchanged.
- **Exceptions.** Failures raise the classes of the new hierarchy, which also derive from
  ``KeyError``, ``IndexError`` or ``ValueError`` where one applies.
- **Removed** the dynamic programming and greedy algorithms.

Added
~~~~~

- ``pydsa.core`` with ``BaseStructure`` and the ``Comparable`` protocol.
- New exceptions: ``NotFoundError``, ``KeyNotFoundError``, ``VertexNotFoundError``,
  ``EdgeNotFoundError``, ``IndexOutOfRangeError``, ``InvalidValueError`` and
  ``InvalidPathError``.
- Binary trees, ``BSTree`` and ``AVLTree`` share ``BinaryTreeBase`` and ``SearchTreeBase``.
- ``MinHeap`` and ``MaxHeap`` share ``HeapBase``.
- ``.pyi`` stubs for the top-level package and every subpackage.

Fixed
~~~~~

- ``Trie.clear`` and ``Trie.starts_with`` with an empty string on an empty trie.

Migrating from 1.x
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 1.x
     - 2.0
   * - ``from pydsa import SinglyList``
     - ``from pydsa.linear import SinglyList``
   * - ``from pydsa import BSTree``
     - ``from pydsa.trees import BSTree``
   * - ``from pydsa import HashTable``
     - ``from pydsa.hash import HashTable``
   * - ``from pydsa import Graph``
     - ``from pydsa.graph import Graph``
   * - ``from pydsa import merge_sort``
     - ``from pydsa.sorting import merge_sort``
   * - ``from pydsa import binary_search``
     - ``from pydsa.searching import binary_search``
   * - ``from pydsa import EmptyError``
     - ``from pydsa.exc import EmptyError``
   * - ``stack.is_empty()``
     - ``not stack``
