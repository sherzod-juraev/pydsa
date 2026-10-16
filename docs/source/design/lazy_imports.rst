Lazy Imports
============

``import pydsa`` loads no submodule. Each package defines ``__getattr__`` and ``__dir__``
(:pep:`562`), together with a table that maps a public name to the module that defines it:

.. code-block:: python

   _LAZY_IMPORTS = {
       "SinglyList": ("singly", "SinglyList"),
       "Stack": ("stack", "Stack"),
   }

The module is imported the first time a name is accessed.

.. code-block:: python

   import sys
   import pydsa

   "pydsa.linear" in sys.modules      # False
   pydsa.linear.Stack
   "pydsa.linear" in sys.modules      # True

Type checkers and IDEs do not run ``__getattr__``. Every package therefore ships a ``.pyi``
stub that re-exports its names in the explicit ``X as X`` form, and the wheel includes
``py.typed``. Completion and static checking see the whole API, while runtime stays lazy.

Only submodules are reachable from the top-level package. A name such as ``Stack`` is
imported from ``pydsa.linear``, never from ``pydsa`` itself.
