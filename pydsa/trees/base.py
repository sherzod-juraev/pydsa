"""Shared foundation of the binary trees.

Provides :class:`BinaryTreeBase`, the parent of every node-based binary tree, and
:class:`SearchTreeBase`, the parent of the binary searching trees. They own the root
and size bookkeeping and every operation that does not depend on how values are
inserted or removed; the subclasses supply only the insertion and removal rules.
"""

from abc import abstractmethod
from collections.abc import Iterator
from typing import cast

from ..core import BaseStructure, Comparable
from ..linear import Queue, Stack


class _BinaryNode[T]:
    """A node holding a value and references to its left and right children.

    Parameters
    ----------
    value : T
        The value to store in this node.

    Attributes
    ----------
    value : T
        The stored value.
    left : _BinaryNode or None
        The left child, or ``None`` if there is none.
    right : _BinaryNode or None
        The right child, or ``None`` if there is none.
    """

    def __init__(self, value: T) -> None:
        """Initialize a leaf node holding the given value."""
        self.value: T = value
        self.left: _BinaryNode[T] | None = None
        self.right: _BinaryNode[T] | None = None


class BinaryTreeBase[T](BaseStructure):
    """Abstract foundation of the node-based binary trees.

    Owns the root node and the node count, and implements everything that only
    needs to walk the existing nodes: the four traversals, ``height``, ``leaves``,
    ``root`` and ``clear``. How nodes are added or removed differs between the
    trees, so ``insert`` and ``remove`` are left to the subclasses.

    Time Complexity Summary

    .. csv-table:: Binary Tree Base Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "root", "O(1)", "O(1)"
       "preorder", "O(n)", "O(h)"
       "inorder", "O(n)", "O(h)"
       "postorder", "O(n)", "O(h)"
       "levelorder", "O(n)", "O(w)"
       "height", "O(n)", "O(w)"
       "leaves", "O(n)", "O(w)"
       "__len__", "O(1)", "O(1)"
       "clear", "O(1)", "O(1)"

    *h = height, w = maximum width of the tree*

    Notes
    -----
    - Not meant to be used directly and not exported from :mod:`pydsa.trees`.
    - Subclasses keep the tree in ``_root`` and ``_size``. A subclass whose nodes
      carry extra data redeclares ``_root`` with its own node type.
    - Every traversal is iterative and lazy. Changing the tree while a traversal is
      running gives undefined results.
    """

    def __init__(self) -> None:
        """Initialize an empty tree."""
        self._root: _BinaryNode[T] | None = None
        self._size: int = 0

    def __len__(self) -> int:
        """Return the number of nodes. O(1)."""
        return self._size

    def clear(self) -> None:
        """Remove all nodes from the tree. O(1)."""
        self._root = None
        self._size = 0

    def root(self) -> T:
        """Return the value of the root node. O(1).

        Raises
        ------
        EmptyError
            If the tree is empty.
        """
        self._ensure_not_empty()
        return cast(_BinaryNode[T], self._root).value

    def preorder(self) -> Iterator[T]:
        """Yield values in preorder traversal (root → left → right). O(n).

        Uses an explicit stack to simulate recursion.

        Returns
        -------
        Iterator
            Values in preorder sequence.
        """
        root = self._root
        if root is None:
            return
        stack: Stack[_BinaryNode[T]] = Stack()
        stack.push(root)
        while stack:
            node = stack.pop()
            yield node.value
            if node.right is not None:
                stack.push(node.right)
            if node.left is not None:
                stack.push(node.left)

    def inorder(self) -> Iterator[T]:
        """Yield values in inorder traversal (left → root → right). O(n).

        Uses an explicit stack to simulate recursion. In a searching tree the
        values come out in ascending order.

        Returns
        -------
        Iterator
            Values in inorder sequence.
        """
        stack: Stack[_BinaryNode[T]] = Stack()
        current = self._root
        while stack or current is not None:
            while current is not None:
                stack.push(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def postorder(self) -> Iterator[T]:
        """Yield values in postorder traversal (left → right → root). O(n).

        Uses an explicit stack and a ``last_visited`` marker to tell when the right
        subtree of a node has been fully processed.

        Returns
        -------
        Iterator
            Values in postorder sequence.
        """
        stack: Stack[_BinaryNode[T]] = Stack()
        current = self._root
        last_visited: _BinaryNode[T] | None = None
        while stack or current is not None:
            if current is not None:
                stack.push(current)
                current = current.left
                continue
            top = stack.peek()
            if top.right is not None and top.right is not last_visited:
                current = top.right
            else:
                last_visited = stack.pop()
                yield last_visited.value

    def levelorder(self) -> Iterator[T]:
        """Yield values in level-order traversal (breadth-first). O(n).

        Uses an explicit queue to visit the nodes level by level.

        Returns
        -------
        Iterator
            Values in level-order sequence.
        """
        root = self._root
        if root is None:
            return
        queue: Queue[_BinaryNode[T]] = Queue()
        queue.enqueue(root)
        while queue:
            node = queue.dequeue()
            yield node.value
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)

    def height(self) -> int:
        """Return the height of the tree in nodes. O(n).

        The height is the number of nodes on the longest path from the root to a
        leaf. A single-node tree has height 1 and an empty tree has height 0.

        Returns
        -------
        int
            The height of the tree.
        """
        root = self._root
        if root is None:
            return 0
        queue: Queue[_BinaryNode[T]] = Queue()
        queue.enqueue(root)
        levels = 0
        while queue:
            for _ in range(len(queue)):
                node = queue.dequeue()
                if node.left is not None:
                    queue.enqueue(node.left)
                if node.right is not None:
                    queue.enqueue(node.right)
            levels += 1
        return levels

    def leaves(self) -> int:
        """Return the number of leaf nodes (nodes without children). O(n).

        Returns
        -------
        int
            The leaf count, ``0`` for an empty tree.
        """
        root = self._root
        if root is None:
            return 0
        queue: Queue[_BinaryNode[T]] = Queue()
        queue.enqueue(root)
        count = 0
        while queue:
            node = queue.dequeue()
            if node.left is None and node.right is None:
                count += 1
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)
        return count


class SearchTreeBase[T: Comparable](BinaryTreeBase[T]):
    """Abstract foundation of the binary searching trees.

    Every node satisfies ``left < node < right``, so a lookup follows a single path
    from the root. This class implements the read-only operations that rely on that
    order; ``insert`` and ``remove`` stay abstract because keeping the tree balanced
    (or not) is exactly what distinguishes the subclasses.

    Time Complexity Summary

    .. csv-table:: Search Tree Base Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "search", "O(h)", "O(1)"
       "min_value", "O(h)", "O(1)"
       "max_value", "O(h)", "O(1)"
       "__contains__", "O(h)", "O(1)"

    *h = height of the tree*

    Notes
    -----
    - Not meant to be used directly and not exported from :mod:`pydsa.trees`.
    - Duplicate values are not stored: inserting a value that is already present
      leaves the tree unchanged.
    - An inorder traversal yields the values in ascending order.
    """

    def __contains__(self, item: T) -> bool:
        """Return True if the value exists in the tree. O(h).

        Uses iterative binary searching from the root.
        """
        current = self._root
        while current is not None:
            if current.value == item:
                return True
            current = current.right if current.value < item else current.left
        return False

    def search(self, value: T, /) -> bool:
        """Return True if the value exists in the tree. O(h).

        Parameters
        ----------
        value : T
            The value to search for.

        Returns
        -------
        bool
            True if found, False otherwise.

        Examples
        --------
        >>> from pydsa.trees import BSTree
        >>> tree = BSTree[int]()
        >>> tree.insert(5)
        >>> tree.search(5)
        True
        >>> tree.search(99)
        False
        """
        return value in self

    def min_value(self) -> T:
        """Return the minimum value in the tree (leftmost node). O(h).

        Returns
        -------
        T
            The smallest value in the tree.

        Raises
        ------
        EmptyError
            If the tree is empty.

        Examples
        --------
        >>> from pydsa.trees import BSTree
        >>> tree = BSTree[int]()
        >>> for value in [5, 3, 8, 1]:
        ...     tree.insert(value)
        >>> tree.min_value()
        1
        """
        self._ensure_not_empty()
        current = cast(_BinaryNode[T], self._root)
        while current.left is not None:
            current = current.left
        return current.value

    def max_value(self) -> T:
        """Return the maximum value in the tree (rightmost node). O(h).

        Returns
        -------
        T
            The largest value in the tree.

        Raises
        ------
        EmptyError
            If the tree is empty.

        Examples
        --------
        >>> from pydsa.trees import BSTree
        >>> tree = BSTree[int]()
        >>> for value in [5, 3, 8, 1]:
        ...     tree.insert(value)
        >>> tree.max_value()
        8
        """
        self._ensure_not_empty()
        current = cast(_BinaryNode[T], self._root)
        while current.right is not None:
            current = current.right
        return current.value

    @abstractmethod
    def insert(self, value: T, /) -> None:
        """Insert a value, keeping the searching order.

        Duplicate values are silently ignored.

        Parameters
        ----------
        value : T
            The value to insert.
        """

    @abstractmethod
    def remove(self, value: T, /) -> None:
        """Remove a value if it exists, keeping the searching order.

        If the value is not found, or the tree is empty, the tree is unchanged.

        Parameters
        ----------
        value : T
            The value to remove.
        """
