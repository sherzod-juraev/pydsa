Trees
=====

Binary trees, two search trees, the binary heaps and the trie. The binary trees share their
traversals, and the heaps share their sift logic, see :doc:`../../design/shared_bases`.

.. grid:: 1 2 2 3
   :gutter: 3
   :padding: 0

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      BinaryTree
      ^^^^^^^^^^
      A plain binary tree. A value is placed by its path of ``L`` and ``R`` steps.

      +++
      .. button-ref:: binary_tree
         :ref-type: doc
         :color: primary
         :expand:

         View BinaryTree

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      BSTree
      ^^^^^^
      Binary search tree. O(h) search, insert and remove, with no rebalancing.

      +++
      .. button-ref:: bst
         :ref-type: doc
         :color: primary
         :expand:

         View BSTree

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      AVLTree
      ^^^^^^^
      Self-balancing search tree. O(log n) search, insert and remove.

      +++
      .. button-ref:: avl_tree
         :ref-type: doc
         :color: primary
         :expand:

         View AVLTree

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      MinHeap / MaxHeap
      ^^^^^^^^^^^^^^^^^
      Binary heaps. O(1) peek and O(log n) insert and extract.

      +++
      .. button-ref:: heap
         :ref-type: doc
         :color: primary
         :expand:

         View the heaps

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Trie
      ^^^^
      Prefix tree for words. Cost depends on the word length, not on the word count.

      +++
      .. button-ref:: trie
         :ref-type: doc
         :color: primary
         :expand:

         View Trie

.. toctree::
   :maxdepth: 1
   :hidden:

   binary_tree
   bst
   avl_tree
   heap
   trie
