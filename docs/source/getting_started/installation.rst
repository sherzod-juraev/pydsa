Installation
============

.. note::

   pydsa requires Python 3.12 or newer and has no external runtime
   dependencies.

.. tab-set::

   .. tab-item:: From GitHub (pip)

      Install directly from GitHub without cloning the repository:

      .. code-block:: bash

         pip install git+https://github.com/sherzod-juraev/pydsa.git@main

   .. tab-item:: Clone + editable install

      Clone the repository and install in editable mode — useful if
      you want to browse or modify the source locally:

      .. code-block:: bash

         git clone https://github.com/sherzod-juraev/pydsa.git
         cd pydsa
         pip install -e .

   .. tab-item:: Development

      Installs pydsa along with pytest, ruff, mypy, and interrogate,
      for running the test suite or contributing. ``nox`` then runs every
      quality check in one command:

      .. code-block:: bash

         git clone https://github.com/sherzod-juraev/pydsa.git
         cd pydsa
         pip install -e ".[dev]"
         nox

Verifying the Installation
--------------------------

Import a structure from its submodule and use it:

.. code-block:: python

   from pydsa.linear import Stack

   stack = Stack[int]()
   stack.push(1)
   print(stack.pop())
   # 1

The version of the installed package is available as ``pydsa.__version__``.

.. tip::

   Continue with the :doc:`quickstart` for a short example of every module.
