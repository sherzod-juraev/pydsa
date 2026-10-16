Exceptions
==========

One hierarchy
-------------

All errors derive from :class:`~pydsa.exc.PydsaError`. A caller can handle any library
failure with one ``except`` clause, and still tell the cases apart by catching a narrower
class.

Also a built-in
---------------

An error that stands in for a built-in exception also derives from it. Code written for the
built-in keeps working, and the library does not force callers to import its own names.

.. list-table::
   :header-rows: 1
   :widths: 32 24 44

   * - Exception
     - Also
     - Meaning
   * - :class:`~pydsa.exc.EmptyError`
     -
     - An element was requested from an empty structure.
   * - :class:`~pydsa.exc.IndexOutOfRangeError`
     - ``IndexError``
     - A position lies outside the structure.
   * - :class:`~pydsa.exc.NotFoundError`
     - ``KeyError``
     - Base of the three errors below.
   * - :class:`~pydsa.exc.KeyNotFoundError`
     - ``KeyError``
     - A key is missing from a mapping.
   * - :class:`~pydsa.exc.VertexNotFoundError`
     - ``KeyError``
     - A vertex is missing from a graph.
   * - :class:`~pydsa.exc.EdgeNotFoundError`
     - ``KeyError``
     - An edge is missing from a graph.
   * - :class:`~pydsa.exc.InvalidValueError`
     - ``ValueError``
     - An argument has the right type but an unusable value.
   * - :class:`~pydsa.exc.InvalidPathError`
     - ``ValueError``
     - A binary tree path is malformed or points to a missing or occupied slot.

Where it lives
--------------

The hierarchy sits in ``pydsa.exc``, a module of its own that imports nothing from the rest
of the library. Any structure can raise any of these errors without creating an import
cycle. The shared emptiness check lives in :doc:`BaseStructure <../api/core>`.
