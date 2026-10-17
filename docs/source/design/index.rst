Design Notes
============

Notes on the decisions behind pydsa: what the library is made of, how its structures
share behavior, and what happens when something goes wrong.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card:: Shared Bases
      :link: shared_bases
      :link-type: doc
      :shadow: sm

      How ``BaseStructure`` and the family bases keep each algorithm in one place.

   .. grid-item-card:: Exceptions
      :link: exceptions
      :link-type: doc
      :shadow: sm

      Why there is one hierarchy, and why each error also is a built-in one.

   .. grid-item-card:: Lazy Imports
      :link: lazy_imports
      :link-type: doc
      :shadow: sm

      Why ``import pydsa`` loads nothing, and how type checkers still see every name.

   .. grid-item-card:: Principles
      :link: principles
      :link-type: doc
      :shadow: sm

      Built from scratch, zero dependencies, clarity over performance.

.. toctree::
   :maxdepth: 1
   :hidden:

   shared_bases
   exceptions
   lazy_imports
   principles
