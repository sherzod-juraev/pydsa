Design Notes
============

Notes on the decisions behind pydsa: what the library is made of, how its structures
share behavior, and what happens when something goes wrong.

.. grid:: 1 2 2 2
   :gutter: 3
   :padding: 0

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Shared Bases
      ^^^^^^^^^^^^
      How ``BaseStructure`` and the family bases keep each algorithm in one place.

      +++
      .. button-ref:: shared_bases
         :ref-type: doc
         :color: primary
         :expand:

         Read about shared bases

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Exceptions
      ^^^^^^^^^^
      Why there is one hierarchy, and why each error also is a built-in one.

      +++
      .. button-ref:: exceptions
         :ref-type: doc
         :color: primary
         :expand:

         Read about exceptions

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Lazy Imports
      ^^^^^^^^^^^^
      Why ``import pydsa`` loads nothing, and how type checkers still see every name.

      +++
      .. button-ref:: lazy_imports
         :ref-type: doc
         :color: primary
         :expand:

         Read about lazy imports

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Principles
      ^^^^^^^^^^
      Built from scratch, zero dependencies, clarity over performance.

      +++
      .. button-ref:: principles
         :ref-type: doc
         :color: primary
         :expand:

         Read the principles

.. toctree::
   :maxdepth: 1
   :hidden:

   shared_bases
   exceptions
   lazy_imports
   principles
