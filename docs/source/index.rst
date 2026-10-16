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

   .. grid-item-card:: ⚙️ Installation
      :link: getting_started/installation
      :link-type: doc
      :text-align: center
      :shadow: md

      Get started in under a minute — no external dependencies.

   .. grid-item-card:: 🚀 Quickstart
      :link: getting_started/quickstart
      :link-type: doc
      :text-align: center
      :shadow: md

      One short, runnable example for every part of the library.

   .. grid-item-card:: 📚 API Reference
      :link: api/index
      :link-type: doc
      :text-align: center
      :shadow: md

      Every structure and algorithm, documented with full type
      signatures and complexity.

   .. grid-item-card:: 🧭 Design Notes
      :link: design/index
      :link-type: doc
      :text-align: center
      :shadow: md

      Why things are built the way they are.

Everything is imported from a submodule, and each submodule is loaded
only when it is first used:

.. code-block:: python

   from pydsa.linear import Stack
   from pydsa.trees import AVLTree
   from pydsa.sorting import merge_sort
