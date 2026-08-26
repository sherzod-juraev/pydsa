Design Notes
==============

Notes on some of the decisions behind pydsa, and what changed along
the way.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: Built from Scratch
      :shadow: sm

      Linked lists, trees, and the ``Stack``/``Queue`` adapters built on
      them manage their own nodes and pointers — no built-in ``list`` or
      ``dict`` underneath their core logic.

      Heaps, ``Graph``, ``Trie``, and ``HashTable`` do use a Python
      ``list`` or ``dict`` as their underlying array or mapping — that's
      the standard building block for those structures (an array *is*
      how a heap is implemented; a mapping *is* how adjacency lists and
      trie children are represented), not a shortcut around the point of
      the library.

   .. grid-item-card:: Zero Dependencies
      :shadow: sm

      pydsa started with numpy in a few DP/greedy functions. It was
      dropped — using it for vectorized array ops didn't fit a
      library whose whole point is showing the algorithm itself.

   .. grid-item-card:: Lazy Imports
      :shadow: sm

      Every package uses ``__getattr__``/``__dir__`` (PEP 562) so
      importing ``pydsa`` doesn't eagerly load every submodule.

   .. grid-item-card:: Clarity over Performance
      :shadow: sm

      Implementations favor being readable and correct over being fast.
      The goal isn't to outperform Python's built-in ``list``/``dict``/
      ``heapq`` — it's to see how the structures work by building them,
      not to replace what already works well.
