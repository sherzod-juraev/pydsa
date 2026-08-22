"""Node type for the singly linked list.

Provides :class:`Node`, an internal building block holding a value and
a reference to the next node in the chain. Not intended for direct use
outside :mod:`pydsa.linear.singly`.
"""


class Node[T]:
    """A single node holding a value and a reference to the next node.

    Parameters
    ----------
    value : T
        The value to store in this node.
    """

    def __init__(self, value: T) -> None:
        """Initialize a node with the given value and no successor."""
        self.value: T = value
        self.next: Node[T] | None = None
