"""AVL tree (self-balancing BST) implementation.

Provides :class:`AVLTree`, a self-balancing binary searching tree that guarantees
O(log n) height via rotations after insertion and removal.
"""

from typing import cast

from ..core import Comparable
from ..linear import Stack
from .base import SearchTreeBase, _BinaryNode


class _AVLNode[T](_BinaryNode[T]):
    """A binary node that also stores the height of its subtree.

    Parameters
    ----------
    value : T
        The value to store in this node.

    Attributes
    ----------
    height : int
        The number of nodes on the longest path from this node down to a leaf. A
        leaf has height 1.
    """

    left: "_AVLNode[T] | None"
    right: "_AVLNode[T] | None"

    def __init__(self, value: T) -> None:
        """Initialize a leaf node (height 1) holding the given value."""
        super().__init__(value)
        self.height: int = 1


def _height[T](node: _AVLNode[T] | None, /) -> int:
    """Return the height of a node, treating ``None`` as 0."""
    return node.height if node is not None else 0


def _update_height[T](node: _AVLNode[T], /) -> None:
    """Recompute the height of a node from the heights of its children."""
    node.height = 1 + max(_height(node.left), _height(node.right))


def _rotate_right[T](node: _AVLNode[T], /) -> _AVLNode[T]:
    """Rotate a subtree to the right (LL case).

    Returns
    -------
    _AVLNode
        The new root of the subtree.
    """
    pivot = cast(_AVLNode[T], node.left)
    node.left = pivot.right
    pivot.right = node
    _update_height(node)
    _update_height(pivot)
    return pivot


def _rotate_left[T](node: _AVLNode[T], /) -> _AVLNode[T]:
    """Rotate a subtree to the left (RR case).

    Returns
    -------
    _AVLNode
        The new root of the subtree.
    """
    pivot = cast(_AVLNode[T], node.right)
    node.right = pivot.left
    pivot.left = node
    _update_height(node)
    _update_height(pivot)
    return pivot


def _rebalance[T](node: _AVLNode[T], /) -> _AVLNode[T]:
    """Update the height of a node and rotate its subtree if it is unbalanced.

    Returns
    -------
    _AVLNode
        The root of the subtree after balancing, which is ``node`` itself when no
        rotation was needed.
    """
    _update_height(node)
    balance = _height(node.left) - _height(node.right)
    if balance > 1:
        left = cast(_AVLNode[T], node.left)
        if _height(left.right) > _height(left.left):
            node.left = _rotate_left(left)
        return _rotate_right(node)
    if balance < -1:
        right = cast(_AVLNode[T], node.right)
        if _height(right.left) > _height(right.right):
            node.right = _rotate_right(right)
        return _rotate_left(node)
    return node


class AVLTree[T: Comparable](SearchTreeBase[T]):
    """A self-balancing binary searching tree (AVL).

    The heights of the two subtrees of every node differ by at most 1. After every
    insertion and removal the nodes on the affected path are checked and rotated
    (LL, RR, LR, RL) to restore that invariant. This guarantees O(log n) height and
    O(log n) searching, insertion and removal in both the average and the worst case.

    Time Complexity Summary

    .. csv-table:: AVL Tree Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "insert", "O(log n)", "O(log n)"
       "remove", "O(log n)", "O(log n)"
       "search", "O(log n)", "O(1)"
       "min_value", "O(log n)", "O(1)"
       "max_value", "O(log n)", "O(1)"
       "preorder", "O(n)", "O(log n)"
       "inorder", "O(n)", "O(log n)"
       "postorder", "O(n)", "O(log n)"
       "levelorder", "O(n)", "O(w)"
       "height", "O(1)", "O(1)"
       "leaves", "O(n)", "O(w)"
       "__contains__", "O(log n)", "O(1)"

    *w = maximum width*

    Notes
    -----
    - Balance factor: ``bf = height(left) - height(right)``.
    - Invariant: ``|bf| <= 1`` for every node.
    - Rotations: right (LL, LR) and left (RR, RL).
    - Duplicate values are silently ignored.
    - All traversals are iterative and use the library's own Stack and Queue.
    """

    _root: _AVLNode[T] | None

    def insert(self, value: T, /) -> None:
        """Insert a value and rebalance the tree. O(log n).

        Duplicate values are silently ignored. The AVL invariant is restored after
        the insertion with rotations if necessary.

        Parameters
        ----------
        value : T
            The value to insert.

        Examples
        --------
        >>> avl = AVLTree[int]()
        >>> for v in [10, 20, 30]:  # would degenerate a plain BST
        ...     avl.insert(v)
        >>> avl.height()  # stays balanced instead of height 3
        2
        """
        if self._root is None:
            self._root = _AVLNode(value)
            self._size += 1
            return
        path: Stack[_AVLNode[T]] = Stack()
        current: _AVLNode[T] | None = self._root
        while current is not None:
            if current.value == value:
                return
            path.push(current)
            current = current.right if current.value < value else current.left
        parent = path.peek()
        if parent.value < value:
            parent.right = _AVLNode(value)
        else:
            parent.left = _AVLNode(value)
        self._size += 1
        self._retrace(path)

    def remove(self, value: T, /) -> None:
        """Remove a value and rebalance the tree. O(log n).

        Handles the three standard BST removal cases (leaf, one child, two
        children) and rotates along the path back to the root to keep the AVL
        invariant.

        If the value is not found, or the tree is empty, the tree is unchanged.

        Parameters
        ----------
        value : T
            The value to remove.

        Examples
        --------
        >>> avl = AVLTree[int]()
        >>> for v in [1, 2, 3, 4]:
        ...     avl.insert(v)
        >>> avl.remove(2)
        >>> list(avl.inorder())
        [1, 3, 4]
        """
        path: Stack[_AVLNode[T]] = Stack()
        current = self._root
        while current is not None and current.value != value:
            path.push(current)
            current = current.left if value < current.value else current.right
        if current is None:
            return
        if current.left is not None and current.right is not None:
            path.push(current)
            successor = current.right
            while successor.left is not None:
                path.push(successor)
                successor = successor.left
            current.value = successor.value
            current = successor
        child = current.left if current.left is not None else current.right
        if not path:
            self._root = child
        else:
            parent = path.peek()
            if current is parent.left:
                parent.left = child
            else:
                parent.right = child
        self._size -= 1
        self._retrace(path)

    def height(self) -> int:
        """Return the height of the tree in nodes. O(1).

        Every node stores the height of its subtree, so the height of the tree is
        read from the root. A single-node tree has height 1 and an empty tree has
        height 0.

        Returns
        -------
        int
            The height of the tree.
        """
        return _height(self._root)

    def _retrace(self, path: Stack[_AVLNode[T]], /) -> None:
        """Rebalance every node on a path, from the deepest one up to the root.

        The path is consumed. A rotation replaces the root of a subtree, so the
        new subtree root is linked back to its parent, or becomes the tree root.

        Parameters
        ----------
        path : Stack
            The nodes from the root down to the parent of the changed position, with
            the deepest node on top.
        """
        while path:
            node = path.pop()
            balanced = _rebalance(node)
            if not path:
                self._root = balanced
            else:
                parent = path.peek()
                if node is parent.left:
                    parent.left = balanced
                else:
                    parent.right = balanced
