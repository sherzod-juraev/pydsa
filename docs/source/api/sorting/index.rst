Sorting
=======

Nine sorting algorithms grouped by strategy: elementary (bubble, selection, insertion),
divide-and-conquer (merge, quick), heap sort, and non-comparison sorts (counting, radix,
bucket). Each is a standalone function, not a class. Every function returns a new list and
leaves its input unchanged.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Elementary
      ^^^^^^^^^^
      Bubble, selection, and insertion sort. O(n²) time — simple to read, not efficient at
      scale.

      +++
      .. button-ref:: elementary
         :ref-type: doc
         :color: primary
         :expand:

         View elementary sorts

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Divide & Conquer
      ^^^^^^^^^^^^^^^^
      Merge sort (O(n log n), stable, O(n) extra space) and quick sort (O(n log n) average,
      O(n²) worst case).

      +++
      .. button-ref:: divide_conquer
         :ref-type: doc
         :color: primary
         :expand:

         View divide & conquer

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Heap Sort
      ^^^^^^^^^
      O(n log n) sort built on :class:`~pydsa.trees.MinHeap`.

      +++
      .. button-ref:: heap
         :ref-type: doc
         :color: primary
         :expand:

         View heap sort

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Linear (Non-Comparison)
      ^^^^^^^^^^^^^^^^^^^^^^^
      Counting, radix, and bucket sort. O(n + k) time under their respective assumptions on
      the input — no element comparisons.

      +++
      .. button-ref:: linear
         :ref-type: doc
         :color: primary
         :expand:

         View non-comparison sorts

.. toctree::
   :maxdepth: 1
   :hidden:

   elementary
   divide_conquer
   heap
   linear
