Linear Structures
=================

Two linked lists and the two adapters built on them. The lists share one implementation
of their algorithms, and ``Stack`` and ``Queue`` expose only their own operations.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: SinglyList
      :link: singly_list
      :link-type: doc
      :text-align: center
      :shadow: sm

      Nodes linked in one direction. O(1) insertion and removal at the front.

   .. grid-item-card:: DoublyList
      :link: doubly_list
      :link-type: doc
      :text-align: center
      :shadow: sm

      Nodes linked in both directions. O(1) at both ends.

   .. grid-item-card:: Stack
      :link: stack
      :link-type: doc
      :text-align: center
      :shadow: sm

      Last in, first out. ``push``, ``pop`` and ``peek`` in O(1).

   .. grid-item-card:: Queue
      :link: queue
      :link-type: doc
      :text-align: center
      :shadow: sm

      First in, first out. ``enqueue``, ``dequeue`` and ``peek`` in O(1).

.. toctree::
   :maxdepth: 1
   :hidden:

   singly_list
   doubly_list
   stack
   queue
