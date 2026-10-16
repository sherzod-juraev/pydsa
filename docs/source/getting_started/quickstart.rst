Quickstart
==========

pydsa is organised in submodules. Import what you need from the submodule that
owns it:

.. code-block:: python

   from pydsa.linear import Stack          # a name from a submodule
   import pydsa
   pydsa.trees.AVLTree                     # or through the package

Nothing is imported until it is first used, see :doc:`../design/lazy_imports`.

Linear structures
-----------------

Stacks, queues and linked lists share one small interface: ``len()``, truthiness and
``clear()``. Taking an element from an empty structure raises :class:`~pydsa.exc.EmptyError`.

.. code-block:: pycon

   >>> from pydsa.linear import SinglyList, Stack
   >>> stack = Stack[int]()
   >>> stack.push(1)
   >>> stack.push(2)
   >>> stack.pop()
   2
   >>> len(stack), bool(stack)
   (1, True)
   >>> stack.clear()
   >>> stack.pop()
   Traceback (most recent call last):
       ...
   pydsa.exc.EmptyError: Stack is empty

   >>> items = SinglyList[int]()
   >>> for value in (1, 2, 3):
   ...     items.insert_last(value)
   >>> items.reverse()
   >>> list(items)
   [3, 2, 1]

Trees and heaps
---------------

Search trees keep their values ordered. Traversals are lazy, so wrap them in ``list()``
to see the values.

.. code-block:: pycon

   >>> from pydsa.trees import AVLTree, MinHeap, Trie
   >>> tree = AVLTree[int]()
   >>> for value in (5, 3, 8, 1):
   ...     tree.insert(value)
   >>> list(tree.inorder())
   [1, 3, 5, 8]
   >>> 3 in tree, 4 in tree
   (True, False)

   >>> heap = MinHeap[int]()
   >>> for value in (5, 1, 3):
   ...     heap.insert(value)
   >>> heap.extract_min()
   1

   >>> words = Trie()
   >>> words.insert("car")
   >>> words.insert("cat")
   >>> sorted(words.words_with_prefix("ca"))
   ['car', 'cat']

Hash table and graph
--------------------

.. code-block:: pycon

   >>> from pydsa.hash import HashTable
   >>> from pydsa.graph import Graph
   >>> table = HashTable[str, int](8)
   >>> table["a"] = 1
   >>> table["a"], table.get("z", 0), "a" in table
   (1, 0, True)

   >>> graph = Graph(directed=False)
   >>> graph.add_edge("a", "b")
   >>> list(graph.bfs("a"))
   ['a', 'b']
   >>> graph.has_path("a", "b")
   True

Sorting and searching
---------------------

Algorithms are plain functions. Sorting returns a new list and never changes its input.
A search returns the index of the target, or ``-1``.

.. code-block:: pycon

   >>> from pydsa.sorting import merge_sort
   >>> from pydsa.searching import binary_search
   >>> data = merge_sort([3, 1, 2])
   >>> data
   [1, 2, 3]
   >>> binary_search(data, 3), binary_search(data, 7)
   (2, -1)

Handling errors
---------------

Every error derives from :class:`~pydsa.exc.PydsaError`, and errors that mirror a built-in
(``KeyError``, ``IndexError``, ``ValueError``) also derive from it.

.. code-block:: pycon

   >>> from pydsa.exc import KeyNotFoundError, PydsaError
   >>> try:
   ...     table["missing"]
   ... except KeyError as error:
   ...     print(type(error).__name__)
   KeyNotFoundError
   >>> issubclass(KeyNotFoundError, PydsaError)
   True

.. tip::

   The full list is on the :doc:`../api/exc` page.
