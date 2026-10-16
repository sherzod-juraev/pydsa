"""Exception hierarchy for pydsa.

All errors raised by the library derive from :class:`PydsaError`, so a single
``except PydsaError`` catches any of them. Related errors share an intermediate base,
so callers can also catch a whole category. Errors that correspond to a built-in
exception also derive from it, so code written for the built-in keeps working::

    PydsaError
    ├── EmptyError
    ├── IndexOutOfRangeError            (also IndexError)
    ├── NotFoundError                   (also KeyError)
    │   ├── KeyNotFoundError
    │   ├── VertexNotFoundError
    │   └── EdgeNotFoundError
    └── InvalidValueError               (also ValueError)
        └── InvalidPathError
"""


class PydsaError(Exception):
    """Base class for all exceptions raised by pydsa.

    Catch this type to handle any error that originates from the library without also
    catching unrelated built-in exceptions.
    """


class EmptyError(PydsaError):
    """Raised when an operation needs an element but the structure is empty.

    Typical cases are removing from, peeking at or reading the root of an empty list,
    stack, queue, tree or heap.
    """


class NotFoundError(PydsaError, KeyError):
    """Base class for errors caused by looking up something that does not exist.

    Catch it to handle a missing key, vertex or edge without caring which kind of
    lookup failed. It is also a ``KeyError``, so handlers written for ``KeyError``
    keep working.
    """

    def __str__(self) -> str:
        """Return the message as written, without the quoting ``KeyError`` adds."""
        return Exception.__str__(self)


class KeyNotFoundError(NotFoundError):
    """Raised when a key is not present in a hash table."""


class VertexNotFoundError(NotFoundError):
    """Raised when a graph operation refers to a vertex that does not exist."""


class EdgeNotFoundError(NotFoundError):
    """Raised when a graph operation refers to an edge that does not exist."""


class IndexOutOfRangeError(PydsaError, IndexError):
    """Raised when a positional index falls outside the valid range of a list.

    Negative indices count from the end and are valid down to minus the length of
    the list. It is also an ``IndexError``, so handlers written for ``IndexError``
    keep working.
    """


class InvalidValueError(PydsaError, ValueError):
    """Base class for errors caused by an argument whose value is unacceptable.

    The argument has the right type but breaks a documented requirement, for example
    a negative integer passed to a sort that accepts only non-negative integers. It is
    also a ``ValueError``, so handlers written for ``ValueError`` keep working.
    """


class InvalidPathError(InvalidValueError):
    """Raised when a path string cannot be followed through a binary tree.

    A path is a sequence of ``'L'`` and ``'R'`` steps from the root. It is invalid
    when an intermediate node along it does not exist.
    """
