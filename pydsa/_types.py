"""Centralized type definitions and protocols for pydsa.

Provides static typing structures, primarily the :class:`Comparable` protocol,
to enforce total ordering constraints across sorting and tree modules.
"""

from typing import Any, Protocol


class Comparable(Protocol):
    """A protocol representing types that support strict total ordering relations.

    Classes implementing this protocol must define all relational comparison
    dunder methods to ensure complete type safety during sorting and spatial
    arrangements in tree-based data structures.
    """

    def __lt__(self, other: Any) -> bool:
        """Return True if self is strictly less than other. O(1)."""
        ...

    def __le__(self, other: Any) -> bool:
        """Return True if self is less than or equal to other. O(1)."""
        ...

    def __gt__(self, other: Any) -> bool:
        """Return True if self is strictly greater than other. O(1)."""
        ...

    def __ge__(self, other: Any) -> bool:
        """Return True if self is greater than or equal to other. O(1)."""
        ...

    def __eq__(self, other: Any) -> bool:
        """Return True if self is equal to other. O(1)."""
        ...
