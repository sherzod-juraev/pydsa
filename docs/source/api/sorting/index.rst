Sorting
=======

Nine sorting algorithms grouped by strategy: elementary (bubble, selection, insertion),
divide-and-conquer (merge, quick), heap sort, and non-comparison sorts (counting, radix,
bucket). Each is a standalone function, not a class. Every function returns a new list and
leaves its input unchanged.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: 🔁 Elementary
      :link: elementary
      :link-type: doc
      :text-align: center
      :shadow: sm

      Bubble, selection, and insertion sort. O(n²) time — simple to read, not efficient at
      scale.

   .. grid-item-card:: ⚔️ Divide & Conquer
      :link: divide_conquer
      :link-type: doc
      :text-align: center
      :shadow: sm

      Merge sort (O(n log n), stable, O(n) extra space) and quick sort (O(n log n) average,
      O(n²) worst case).

   .. grid-item-card:: 🌳 Heap Sort
      :link: heap
      :link-type: doc
      :text-align: center
      :shadow: sm

      O(n log n) sort built on :class:`~pydsa.trees.MinHeap`.

   .. grid-item-card:: 🔢 Linear (Non-Comparison)
      :link: linear
      :link-type: doc
      :text-align: center
      :shadow: sm

      Counting, radix, and bucket sort. O(n + k) time under their respective assumptions on
      the input — no element comparisons.

.. toctree::
   :maxdepth: 1
   :hidden:

   elementary
   divide_conquer
   heap
   linear
