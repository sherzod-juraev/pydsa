"""Binary searching tree (BST) implementation.

Provides :class:`BSTree`, an unbalanced binary searching tree with the
``left < node < right`` invariant, supporting insertion, removal, searching and the
four traversal strategies.
"""

from ..core import Comparable
from .base import SearchTreeBase, _BinaryNode


class BSTree[T: Comparable](SearchTreeBase[T]):
    """A binary searching tree (BST).

    Each node satisfies the invariant ``left < node < right``. Values are placed by
    comparison with the existing nodes, and duplicate values are silently ignored.
    The tree is not rebalanced, so its shape depends on the insertion order.

    Time Complexity Summary

    .. csv-table:: BST Operations Complexity
       :header: "Operation", "Time (avg)", "Time (worst)", "Space"
       :widths: 20, 12, 12, 10

       "insert", "O(log n)", "O(n)", "O(1)"
       "remove", "O(log n)", "O(n)", "O(1)"
       "search", "O(log n)", "O(n)", "O(1)"
       "min_value", "O(log n)", "O(n)", "O(1)"
       "max_value", "O(log n)", "O(n)", "O(1)"
       "preorder", "O(n)", "O(n)", "O(h)"
       "inorder", "O(n)", "O(n)", "O(h)"
       "postorder", "O(n)", "O(n)", "O(h)"
       "levelorder", "O(n)", "O(n)", "O(w)"
       "height", "O(n)", "O(n)", "O(w)"
       "leaves", "O(n)", "O(n)", "O(w)"
       "__contains__", "O(log n)", "O(n)", "O(1)"

    *h = height, w = maximum width*

    Notes
    -----
    - An **inorder** traversal yields the values in ascending order.
    - Degenerate trees (for example, inserting already sorted data) reduce the
      performance to O(n). For guaranteed O(log n), see ``AVLTree``.
    - All traversals are iterative and use the library's own Stack and Queue.
    """

    def insert(self, value: T, /) -> None:
        """Insert a value into the tree. O(h).

        Duplicate values are silently ignored. Values less than a node go left and
        greater values go right, so the BST invariant is preserved.

        Parameters
        ----------
        value : T
            The value to insert.

        Examples
        --------
        >>> bst = BSTree[int]()
        >>> bst.insert(5)
        >>> bst.insert(3)
        >>> bst.insert(8)
        >>> bst.insert(3)  # duplicate, ignored
        >>> len(bst)
        3
        """
        if self._root is None:
            self._root = _BinaryNode(value)
            self._size += 1
            return
        current = self._root
        while True:
            if current.value == value:
                return
            if current.value < value:
                if current.right is None:
                    current.right = _BinaryNode(value)
                    break
                current = current.right
            else:
                if current.left is None:
                    current.left = _BinaryNode(value)
                    break
                current = current.left
        self._size += 1

    def remove(self, value: T, /) -> None:
        """Remove a value from the tree if it exists. O(h).

        Handles three cases:

        1. The node is a leaf: it is simply removed.
        2. The node has one child: the child takes its place.
        3. The node has two children: its value is replaced by the inorder
           successor (the smallest value in the right subtree), and the successor
           node is removed instead.

        If the value is not found, or the tree is empty, the tree is unchanged.

        Parameters
        ----------
        value : T
            The value to remove.

        Examples
        --------
        >>> bst = BSTree[int]()
        >>> for v in [5, 3, 8, 1, 4, 7, 9]:
        ...     bst.insert(v)
        >>> bst.remove(5)
        >>> 5 in bst
        False
        >>> list(bst.inorder())
        [1, 3, 4, 7, 8, 9]
        """
        parent: _BinaryNode[T] | None = None
        current = self._root
        while current is not None and current.value != value:
            parent = current
            current = current.left if value < current.value else current.right
        if current is None:
            return
        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.value = successor.value
            parent = successor_parent
            current = successor
        child = current.left if current.left is not None else current.right
        if parent is None:
            self._root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child
        self._size -= 1
