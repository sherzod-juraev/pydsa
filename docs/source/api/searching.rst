Searching
=========

Four search algorithms — linear (unsorted input) through exponential (unbounded input).
Each is a plain function that returns the index of the target, or ``-1`` when it is not
present, and documents its own preconditions on the input.

.. list-table:: At a glance
   :header-rows: 1
   :widths: 28 18 14 40

   * - Algorithm
     - Time
     - Space
     - Requires
   * - :func:`~pydsa.searching.linear_search`
     - O(n)
     - O(1)
     - nothing
   * - :func:`~pydsa.searching.binary_search`
     - O(log n)
     - O(1)
     - ascending order
   * - :func:`~pydsa.searching.jump_search`
     - O(√n)
     - O(1)
     - ascending order
   * - :func:`~pydsa.searching.exponential_search`
     - O(log n)
     - O(1)
     - ascending order

Linear Search
-------------

.. autofunction:: pydsa.searching.linear_search

Binary Search
-------------

.. autofunction:: pydsa.searching.binary_search

Jump Search
-----------

.. autofunction:: pydsa.searching.jump_search

Exponential Search
------------------

.. autofunction:: pydsa.searching.exponential_search
