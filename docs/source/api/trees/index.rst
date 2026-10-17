Trees
=====

Binary trees, two search trees, the binary heaps and the trie. The binary trees share their
traversals, and the heaps share their sift logic, see :doc:`../../design/shared_bases`.

.. grid:: 1 2 2 3
   :gutter: 3
   :padding: 0

   .. grid-item-card:: BinaryTree
      :link: binary_tree
      :link-type: doc
      :text-align: center
      :shadow: sm

      A plain binary tree. A value is placed by its path of ``L`` and ``R`` steps.

   .. grid-item-card:: BSTree
      :link: bst
      :link-type: doc
      :text-align: center
      :shadow: sm

      Binary search tree. O(h) search, insert and remove, with no rebalancing.

   .. grid-item-card:: AVLTree
      :link: avl_tree
      :link-type: doc
      :text-align: center
      :shadow: sm

      Self-balancing search tree. O(log n) search, insert and remove.

   .. grid-item-card:: MinHeap / MaxHeap
      :link: heap
      :link-type: doc
      :text-align: center
      :shadow: sm

      Binary heaps. O(1) peek and O(log n) insert and extract.

   .. grid-item-card:: Trie
      :link: trie
      :link-type: doc
      :text-align: center
      :shadow: sm

      Prefix tree for words. Cost depends on the word length, not on the word count.

.. toctree::
   :maxdepth: 1
   :hidden:

   binary_tree
   bst
   avl_tree
   heap
   trie
