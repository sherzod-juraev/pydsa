Installation
==============

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
      for running the test suite or contributing:

      .. code-block:: bash

         git clone https://github.com/sherzod-juraev/pydsa.git
         cd pydsa
         pip install -e ".[dev]"

Verifying the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pydsa import Stack

   s = Stack[int]()
   s.push(1)
   print(s.pop())
   # 1
