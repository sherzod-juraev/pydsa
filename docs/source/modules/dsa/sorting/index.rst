Sorting
=======

Nine sorting algorithms grouped by strategy: elementary (bubble,
selection, insertion), divide-and-conquer (merge, quick), heap
sort, and non-comparison sorts (counting, radix, bucket). Each is
a standalone function, not a class.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: 🔁 Elementary
      :link: elementary
      :link-type: doc
      :text-align: center
      :shadow: sm

      Bubble, selection, and insertion sort. O(n²) time, O(1)
      extra space — simple to read, not efficient at scale.

   .. grid-item-card:: ⚔️ Divide & Conquer
      :link: divide_conquer
      :link-type: doc
      :text-align: center
      :shadow: sm

      Merge sort (O(n log n), stable, O(n) extra space) and quick
      sort (O(n log n) average, in-place, O(n²) worst case).

   .. grid-item-card:: 🌳 Heap Sort
      :link: heap
      :link-type: doc
      :text-align: center
      :shadow: sm

      In-place O(n log n) sort built on a binary heap. Not stable.

   .. grid-item-card:: 🔢 Linear (Non-Comparison)
      :link: linear
      :link-type: doc
      :text-align: center
      :shadow: sm

      Counting, radix, and bucket sort. O(n + k) time under their
      respective assumptions on the input — no element comparisons.

.. toctree::
   :maxdepth: 1
   :hidden:

   elementary
   divide_conquer
   heap
   linear
