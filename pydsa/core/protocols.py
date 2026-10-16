"""Structural typing contracts shared across pydsa.

Defines :class:`Comparable`, the protocol that bounds the type parameter of every
order-dependent structure and algorithm (search trees, heaps, sorting and searching).
"""

from typing import Any, Protocol


class Comparable(Protocol):
    """Protocol for values that support the full set of comparison operators.

    A type is :class:`Comparable` when it defines ``<``, ``<=``, ``>``, ``>=`` and ``==``
    consistently with a single total order. pydsa uses it as the upper bound of type
    parameters (for example ``T: Comparable``), so a type checker can reject element
    types that cannot be ordered. The built-in ``int``, ``float`` and ``str`` already
    satisfy it.

    Notes
    -----
    - The protocol is checked statically only. It is not ``runtime_checkable``, so
      ``isinstance(value, Comparable)`` raises ``TypeError``.
    - The five operations must agree with each other: ``a <= b`` holds exactly when
      ``a < b`` or ``a == b``, and the order must be transitive. The protocol cannot
      enforce this. A type that breaks it makes sorting and tree operations return
      wrong results without raising an error.

    Examples
    --------
    A dataclass declared with ``order=True`` generates all comparison operators:

    >>> from dataclasses import dataclass
    >>> @dataclass(order=True)
    ... class Version:
    ...     major: int
    ...     minor: int
    >>> Version(1, 2) < Version(1, 10)
    True
    >>> Version(2, 0) >= Version(1, 99)
    True
    """

    def __lt__(self, other: Any) -> bool:
        """Return ``True`` if this value orders strictly before ``other``."""
        ...

    def __le__(self, other: Any) -> bool:
        """Return ``True`` if this value orders before ``other`` or equal to it."""
        ...

    def __gt__(self, other: Any) -> bool:
        """Return ``True`` if this value orders strictly after ``other``."""
        ...

    def __ge__(self, other: Any) -> bool:
        """Return ``True`` if this value orders after ``other`` or equal to it."""
        ...

    def __eq__(self, other: Any) -> bool:
        """Return ``True`` if this value equals ``other`` under the same order."""
        ...
