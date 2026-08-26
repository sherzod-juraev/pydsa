Searching
=========

Four search algorithms — linear (unsorted input) through exponential
(unbounded input) — each documenting its own preconditions on the
input.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: 🔍 Linear Search
      :link: linear_search
      :link-type: doc
      :text-align: center
      :shadow: sm

      Checks each element sequentially. O(n) time, O(1) space.
      Works on unsorted input, no preprocessing required.

   .. grid-item-card:: 🎯 Binary Search
      :link: binary_search
      :link-type: doc
      :text-align: center
      :shadow: sm

      Halves the search interval each step. O(log n) time, O(1)
      space. Requires the input sorted in ascending order.

   .. grid-item-card:: 🦘 Jump Search
      :link: jump_search
      :link-type: doc
      :text-align: center
      :shadow: sm

      Jumps in fixed intervals, then linear-searches the block.
      O(√n) time, O(1) space. Requires sorted ascending input.

   .. grid-item-card:: 📈 Exponential Search
      :link: exponential_search
      :link-type: doc
      :text-align: center
      :shadow: sm

      Finds a bounding range by doubling (1, 2, 4, ...), then
      binary-searches within it. O(log n) time, O(1) space.
      Requires sorted ascending input.

.. toctree::
   :hidden:

   linear_search
   binary_search
   jump_search
   exponential_search
