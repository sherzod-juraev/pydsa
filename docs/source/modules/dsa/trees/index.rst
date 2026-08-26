Trees
=====

From an unordered general tree to a self-balancing search tree, plus
heaps and a trie. Ordered roughly from simplest to most involved —
:doc:`binary_tree` has no invariant to maintain, :doc:`avl_tree` has
the most.

.. grid:: 1 2 2 3
   :gutter: 3
   :padding: 0

   .. grid-item-card:: 🌲 Binary Tree
      :link: binary_tree
      :link-type: doc
      :text-align: center
      :shadow: sm

      Path-based insertion (e.g. ``"LLR"``), four traversal
      strategies. No ordering invariant between nodes.

   .. grid-item-card:: 🔎 BST
      :link: bst
      :link-type: doc
      :text-align: center
      :shadow: sm

      Nodes ordered by ``left < root < right``, insertion driven by
      comparison. O(log n) average, O(n) worst case per operation.

   .. grid-item-card:: ⚖️ AVL Tree
      :link: avl_tree
      :link-type: doc
      :text-align: center
      :shadow: sm

      Self-balancing BST — subtree heights differ by at most 1,
      restored via rotations. O(log n) worst case for every
      operation.

   .. grid-item-card:: 📊 Heap
      :link: heap
      :link-type: doc
      :text-align: center
      :shadow: sm

      Min-heap and max-heap on a dynamic array. Root access is
      O(1); insert and extract are O(log n).

   .. grid-item-card:: 🔤 Trie
      :link: trie
      :link-type: doc
      :text-align: center
      :shadow: sm

      Prefix tree for strings — each node is one character, shared
      prefixes cut memory use. Insert/search are O(L) in the key
      length.

.. toctree::
   :hidden:

   binary_tree
   bst
   avl_tree
   heap
   trie
