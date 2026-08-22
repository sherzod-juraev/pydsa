"""Node type for the trie.

Provides :class:`Node`, an internal building block holding a
character-to-child mapping and an end-of-word marker. Not intended
for direct use outside :mod:`pydsa.trees.trie`.
"""


class Node:
    """A single trie node holding child references and an end marker."""

    def __init__(self) -> None:
        """Initialize a node with no children and not marking a word end."""
        self.children: dict[str, Node] = {}
        self.is_end: bool = False

    def __len__(self) -> int:
        """Return the number of children. O(1)."""
        return len(self.children)

    def __bool__(self) -> bool:
        """Return True if the node has at least one child. O(1)."""
        return len(self) > 0
