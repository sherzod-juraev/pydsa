Core
====

Building blocks shared by every structure. ``Comparable`` is the one a user meets
directly, as the bound of ``T`` in ordered structures and algorithms.
``BaseStructure`` is what a structure derives from. The methods it provides show up on
every structure, see :doc:`../design/shared_bases`.

BaseStructure
-------------

.. autoclass:: pydsa.core.BaseStructure
   :members:

Comparable
----------

.. autoclass:: pydsa.core.Comparable
   :members:
   :special-members: __lt__, __le__, __gt__, __ge__, __eq__
