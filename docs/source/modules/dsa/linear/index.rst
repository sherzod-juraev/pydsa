Linear Data Structures
=======================

Singly and doubly linked lists, and the ``Stack``/``Queue`` adapters
built on top of them. Nothing here delegates storage to Python's
built-in ``list`` — each node and pointer is managed explicitly.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: 🔗 Singly Linked List
      :link: singly_list
      :link-type: doc
      :text-align: center
      :shadow: sm

      Head/tail pointers with O(1) insertion and removal at both
      ends. O(n) for indexed access and insertion/removal at an
      arbitrary position.

   .. grid-item-card:: 🔗 Doubly Linked List
      :link: doubly_list
      :link-type: doc
      :text-align: center
      :shadow: sm

      Bidirectional traversal via next/prev references. O(1)
      removal at both ends; indexed access walks from whichever
      end is closer.

   .. grid-item-card:: 📥 Stack
      :link: stack
      :link-type: doc
      :text-align: center
      :shadow: sm

      LIFO, built on a singly linked list. push, pop, and peek are
      all O(1) via head-insertion and head-removal.

   .. grid-item-card:: 📤 Queue
      :link: queue
      :link-type: doc
      :text-align: center
      :shadow: sm

      FIFO, built on a singly linked list with a maintained tail
      pointer. enqueue and dequeue are both O(1).

.. toctree::
   :maxdepth: 1
   :hidden:

   singly_list
   doubly_list
   stack
   queue
