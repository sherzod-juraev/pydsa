"""Node type for the doubly linked list.

Provides :class:`Node`, an internal building block holding a value and
references to both the next and previous nodes. Not intended for
direct use outside :mod:`pydsa.linear.doubly`.
"""


class Node[T]:
    """A single node holding a value and references to its neighbors.

    Parameters
    ----------
    value : T
        The value to store in this node.
    """

    def __init__(self, value: T) -> None:
        """Initialize a node with the given value and no neighbors."""
        self.value: T = value
        self.next: Node[T] | None = None
        self.prev: Node[T] | None = None
