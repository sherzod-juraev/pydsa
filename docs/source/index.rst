.. meta::
   :description: pydsa is a pure Python, zero-dependency, fully typed library of data structures
      and algorithms built from scratch for studying how they work.

pydsa
=====

Pure Python implementations of fundamental data structures and
algorithms — built from scratch, fully typed, and tested.

.. toctree::
   :hidden:

   getting_started/installation
   getting_started/quickstart
   api/index
   design/index
   changelog

.. grid:: 1 2 2 4
   :gutter: 3
   :class-container: sd-mb-4

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Installation
      ^^^^^^^^^^^^
      Get started in under a minute — no external dependencies.

      +++
      .. button-ref:: getting_started/installation
         :ref-type: doc
         :color: primary
         :expand:

         Get started

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Quickstart
      ^^^^^^^^^^
      One short, runnable example for every part of the library.

      +++
      .. button-ref:: getting_started/quickstart
         :ref-type: doc
         :color: primary
         :expand:

         Try the quickstart

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      API Reference
      ^^^^^^^^^^^^^
      Every structure and algorithm, documented with full type
      signatures and complexity.

      +++
      .. button-ref:: api/index
         :ref-type: doc
         :color: primary
         :expand:

         Browse the API

   .. grid-item-card::
      :text-align: center
      :shadow: sm

      Design Notes
      ^^^^^^^^^^^^
      Why things are built the way they are.

      +++
      .. button-ref:: design/index
         :ref-type: doc
         :color: primary
         :expand:

         Read the notes

Everything is imported from a submodule, and each submodule is loaded
only when it is first used:

.. code-block:: python

   from pydsa.linear import Stack
   from pydsa.trees import AVLTree
   from pydsa.sorting import merge_sort
