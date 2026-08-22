"""Node type for the general binary tree.

Provides :class:`Node`, an internal building block holding a value
and references to its left and right children. Not intended for
direct use outside :mod:`pydsa.trees.binary_tree`.
"""


class Node[T]:
    """A single node holding a value and references to two children.

    Parameters
    ----------
    value : T
        The value to store in this node.
    """

    def __init__(self, value: T) -> None:
        """Initialize a node with the given value and no children."""
        self.value: T = value
        self.left: Node[T] | None = None
        self.right: Node[T] | None = None
