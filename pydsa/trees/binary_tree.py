"""General binary tree implementation.

Provides :class:`BinaryTree`, a general binary tree built by inserting values at
explicit paths, with the four traversal strategies (preorder, inorder, postorder,
level-order).
"""

from ..exc import InvalidPathError
from .base import BinaryTreeBase, _BinaryNode


class BinaryTree[T](BinaryTreeBase[T]):
    """A general binary tree with path-based insertion.

    Nodes are inserted by giving a path string (for example ``"LLR"``) from the
    root: ``'L'`` goes to the left child and ``'R'`` to the right one. A value is
    always attached at an empty position, so inserting never moves or replaces an
    existing node. The tree supports preorder, inorder and postorder traversal
    (iterative, O(n) time, O(h) space) and level-order traversal (BFS, O(n) time,
    O(w) space).

    Time Complexity Summary

    .. csv-table:: Binary Tree Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "insert", "O(h)", "O(1)"
       "preorder", "O(n)", "O(h)"
       "inorder", "O(n)", "O(h)"
       "postorder", "O(n)", "O(h)"
       "levelorder", "O(n)", "O(w)"
       "height", "O(n)", "O(w)"
       "leaves", "O(n)", "O(w)"
       "root", "O(1)", "O(1)"
       "__len__", "O(1)", "O(1)"
       "clear", "O(1)", "O(1)"

    *h = height, w = maximum width of the tree*

    Notes
    -----
    This is a general binary tree without ordering constraints. For a binary
    searching tree with the ``left < node < right`` invariant, see ``BSTree``.
    """

    def insert(self, value: T, path: str, /) -> None:
        """Insert a value at the empty position given by a path string. O(h).

        The path is a sequence of ``'L'`` and ``'R'`` characters read from the
        root. All its nodes except the last must exist, and the position it ends at
        must be empty. An empty path targets the root, which is only allowed while
        the tree is empty. The tree is unchanged when an error is raised.

        Parameters
        ----------
        value : T
            The value to insert.
        path : str
            Path from the root, for example ``"LLR"`` for left, left, right. Only
            uppercase ``'L'`` and ``'R'`` are accepted. An empty string targets the
            root.

        Raises
        ------
        InvalidPathError
            If the path contains a character other than ``'L'`` or ``'R'``, if a
            node along the path is missing, or if the target position is already
            occupied.

        Examples
        --------
        >>> tree = BinaryTree[int]()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> list(tree.levelorder())
        [5, 3, 8, 1]
        """
        if set(path) - {"L", "R"}:
            raise InvalidPathError(f"Path {path!r} may only contain 'L' and 'R'")
        if not path:
            if self._root is not None:
                raise InvalidPathError("Root already exists")
            self._root = _BinaryNode(value)
            self._size += 1
            return
        if self._root is None:
            raise InvalidPathError(f"Path {path!r} does not exist in an empty tree")
        parent = self._root
        for step in path[:-1]:
            child = parent.left if step == "L" else parent.right
            if child is None:
                raise InvalidPathError(f"Path {path!r} is broken: a node on it is missing")
            parent = child
        if path[-1] == "L":
            if parent.left is not None:
                raise InvalidPathError(f"Position {path!r} is already occupied")
            parent.left = _BinaryNode(value)
        else:
            if parent.right is not None:
                raise InvalidPathError(f"Position {path!r} is already occupied")
            parent.right = _BinaryNode(value)
        self._size += 1
