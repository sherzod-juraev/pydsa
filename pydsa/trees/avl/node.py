"""Node type for the AVL tree.

Provides :class:`Node`, an internal building block holding a value,
references to its two children, and its subtree height. Not intended
for direct use outside :mod:`pydsa.trees.avl`.
"""


class Node[T]:
    """A single AVL node holding a value, two children, and its height.

    Parameters
    ----------
    value : T
        The value to store in this node.
    """

    def __init__(self, value: T) -> None:
        """Initialize a leaf node (height 1) with the given value."""
        self.value: T = value
        self.left: Node[T] | None = None
        self.right: Node[T] | None = None
        self.height: int = 1
