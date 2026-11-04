Linear Structures
=================

Two linked lists and the two adapters built on them. The lists share one implementation
of their algorithms, and ``Stack`` and ``Queue`` expose only their own operations.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      SinglyList
      ^^^^^^^^^^
      Nodes linked in one direction. O(1) insertion and removal at the front.

      +++
      .. button-ref:: singly_list
         :ref-type: doc
         :color: primary
         :expand:

         View SinglyList

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      DoublyList
      ^^^^^^^^^^
      Nodes linked in both directions. O(1) at both ends.

      +++
      .. button-ref:: doubly_list
         :ref-type: doc
         :color: primary
         :expand:

         View DoublyList

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Stack
      ^^^^^
      Last in, first out. ``push``, ``pop`` and ``peek`` in O(1).

      +++
      .. button-ref:: stack
         :ref-type: doc
         :color: primary
         :expand:

         View Stack

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Queue
      ^^^^^
      First in, first out. ``enqueue``, ``dequeue`` and ``peek`` in O(1).

      +++
      .. button-ref:: queue
         :ref-type: doc
         :color: primary
         :expand:

         View Queue

.. toctree::
   :maxdepth: 1
   :hidden:

   singly_list
   doubly_list
   stack
   queue
