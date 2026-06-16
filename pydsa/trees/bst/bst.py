from collections.abc import Iterator
from typing import cast

from ..._types import Comparable
from ...exc import EmptyError
from ...linear import Queue, Stack
from ..binary_tree.node import Node


class BSTree[T: Comparable]:
    """
    A binary searching tree (BST) where each node satisfies the invariant
    ``left < root < right``.

    Values are inserted automatically based on comparison with existing
    nodes. Duplicate values are silently ignored. The tree supports
    insertion, deletion, searching, and four traversal strategies, all
    implemented iteratively using custom Stack and Queue ADTs.

    Time Complexity
    .. csv-table:: BST Operations Complexity
       :header: "Operation", "Time (avg)", "Time (worst)", "Space"
       :widths: 20, 12, 12, 10

       "insert", "O(log n)", "O(n)", "O(1)"
       "searching", "O(log n)", "O(n)", "O(1)"
       "min_value", "O(log n)", "O(n)", "O(1)"
       "max_value", "O(log n)", "O(n)", "O(1)"
       "remove", "O(log n)", "O(n)", "O(1)"
       "preorder", "O(n)", "O(n)", "O(h)"
       "inorder", "O(n)", "O(n)", "O(h)"
       "postorder", "O(n)", "O(n)", "O(h)"
       "levelorder", "O(n)", "O(n)", "O(w)"
       "height", "O(n)", "O(n)", "O(w)"
       "__contains__", "O(log n)", "O(n)", "O(1)"

    *h = height, w = maximum width*

    Notes
    -----
    - An **inorder** traversal yields values in sorted ascending order.
    - Degenerate trees (e.g., inserting already-sorted data) reduce
      performance to O(n). For guaranteed O(log n), see ``AVLTree``.
    - Duplicate values are silently ignored during insertion and
      do not affect the tree structure.
    """

    def __init__(self) -> None:

        self.__root: Node[T] | None = None
        self.__nodes: int = 0

    def __len__(self) -> int:
        """Return the number of nodes. O(1)."""
        return self.__nodes

    def __bool__(self) -> bool:
        """Return True if the tree is not empty. O(1)."""
        return self.__nodes > 0

    def __contains__(self, item: T) -> bool:
        """Return True if the value exists in the tree. O(h).

        Uses iterative binary searching from the root.
        """
        current = self.__root
        while current is not None:
            if current.value == item:
                return True
            elif current.value < item:
                current = current.right
            else:
                current = current.left
        return False

    def is_empty(self) -> bool:
        """Return True if the tree has no nodes. O(1)."""
        return self.__nodes == 0

    def root(self) -> T:
        """Return the value of the root node. O(1).

        Raises
        ------
        EmptyError
            If the tree is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        root = cast(Node[T], self.__root)
        return root.value

    def insert(self, value: T, /) -> None:
        """Insert a value into the tree. O(h).

        Duplicate values are silently ignored. The BST invariant
        is preserved: values less than a node go left, greater
        values go right.

        Parameters
        ----------
        value : Any
            The value to insert.

        Examples
        --------
        >>> bst = BSTree()
        >>> bst.insert(5)
        >>> bst.insert(3)
        >>> bst.insert(8)
        >>> bst.insert(3)  # duplicate — ignored
        >>> len(bst)
        3
        """
        if self.is_empty():
            self.__root = Node(value)
            self.__nodes += 1
            return
        current: Node[T] = cast(Node[T], self.__root)
        while current is not None:
            if current.value == value:
                return
            elif current.value < value:
                if current.right is None:
                    current.right = Node(value)
                    self.__nodes += 1
                    return
                current = current.right
            else:
                if current.left is None:
                    current.left = Node(value)
                    self.__nodes += 1
                    return
                current = current.left

    def search(self, value: T, /) -> bool:
        """Return True if the value exists in the tree. O(h).

        Parameters
        ----------
        value : Any
            The value to searching for.

        Returns
        -------
        bool
            True if found, False otherwise.

        Examples
        --------
        >>> bst.searching(5)
        True
        >>> bst.searching(99)
        False
        """
        return value in self

    def min_value(self) -> T:
        """Return the minimum value in the tree (leftmost node). O(h).

        Returns
        -------
        Any
            The smallest value in the tree.

        Raises
        ------
        EmptyError
            If the tree is empty.

        Examples
        --------
        >>> bst.min_value()
        1
        """
        if self.is_empty():
            raise EmptyError(self)
        current: Node[T] = cast(Node[T], self.__root)
        while current.left:
            current = current.left
        return current.value

    def max_value(self) -> T:
        """Return the maximum value in the tree (rightmost node). O(h).

        Returns
        -------
        Any
            The largest value in the tree.

        Raises
        ------
        EmptyError
            If the tree is empty.

        Examples
        --------
        >>> bst.max_value()
        14
        """
        if self.is_empty():
            raise EmptyError(self)
        current: Node[T] = cast(Node[T], self.__root)
        while current.right:
            current = current.right
        return current.value

    def remove(self, value: T, /) -> None:
        """Remove a value from the tree if it exists. O(h).

        Handles three cases:
        1. Node is a leaf — simply removed.
        2. Node has one child — child replaces it.
        3. Node has two children — replaced by its inorder successor
           (smallest value in right subtree).

        If the value is not found, the tree is unchanged.

        Parameters
        ----------
        value : Any
            The value to remove.

        Examples
        --------
        >>> bst.remove(5)
        >>> 5 in bst
        False
        """
        if self.is_empty():
            return
        parent: Node[T] | None = None
        current: Node[T] | None = self.__root
        while current and current.value != value:
            parent = current
            current = current.left if value < current.value else current.right
        if current is None:
            return
        if current.left is not None and current.right is not None:
            successor_parent: Node[T] = current
            successor: Node[T] = current.right
            while successor.left:
                successor_parent = successor
                successor = successor.left
            current.value = successor.value
            parent = successor_parent
            current = successor
        child = current.left if current.left else current.right
        if parent is None:
            self.__root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child
        self.__nodes -= 1

    def preorder(self) -> Iterator[T]:
        """Yield values in preorder traversal (root → left → right). O(n).

        Returns
        -------
        Iterator
            Values in preorder sequence.

        Examples
        --------
        >>> list(bst.preorder())
        [5, 3, 1, 4, 8, 7, 9]
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        stack.push(cast(Node[T], self.__root))
        while stack:
            node: Node[T] = stack.pop()
            yield node.value
            if node.right is not None:
                stack.push(node.right)
            if node.left is not None:
                stack.push(node.left)

    def inorder(self) -> Iterator[T]:
        """Yield values in inorder traversal (left → root → right). O(n).

        Because this is a BST, the output is sorted in ascending order.

        Returns
        -------
        Iterator
            Values in sorted ascending order.

        Examples
        --------
        >>> list(bst.inorder())
        [1, 3, 4, 5, 7, 8, 9]
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        current: Node[T] | None = self.__root
        while stack or current is not None:
            while current is not None:
                stack.push(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def postorder(self) -> Iterator[T]:
        """Yield values in postorder traversal (left → right → root). O(n).

        Returns
        -------
        Iterator
            Values in postorder sequence.

        Examples
        --------
        >>> list(bst.postorder())
        [1, 4, 3, 7, 9, 8, 5]
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        current: Node[T] | None = self.__root
        last_visited: Node[T] | None = None
        while stack or current:
            if current is not None:
                stack.push(current)
                current = current.left
            else:
                peek_node: Node[T] = stack.peek()
                if peek_node.right and peek_node.right != last_visited:
                    current = peek_node.right
                else:
                    last_visited = stack.pop()
                    yield last_visited.value
                    current = None

    def levelorder(self) -> Iterator[T]:
        """Yield values in level-order (breadth-first) traversal. O(n).

        Returns
        -------
        Iterator
            Values in level-order sequence.

        Examples
        --------
        >>> list(bst.levelorder())
        [5, 3, 8, 1, 4, 7, 9]
        """
        if self.is_empty():
            return
        queue: Queue[Node[T]] = Queue()
        queue.enqueue(cast(Node[T], self.__root))
        while queue:
            node: Node[T] = queue.dequeue()
            yield node.value
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)

    def height(self) -> int:
        """Return the height of the tree (nodes on the longest path). O(n).

        A single-node tree has height 1. An empty tree has height 0.

        Returns
        -------
        int
            Height of the tree in nodes.

        Examples
        --------
        >>> bst.height()
        3
        """
        if self.is_empty():
            return 0
        queue: Queue[Node[T]] = Queue()
        queue.enqueue(cast(Node[T], self.__root))
        height = 0
        while queue:
            for _ in range(len(queue)):
                node: Node[T] = queue.dequeue()
                if node.left is not None:
                    queue.enqueue(node.left)
                if node.right is not None:
                    queue.enqueue(node.right)
            height += 1
        return height

    def clear(self) -> None:
        """Remove all nodes from the tree. O(1)."""
        self.__root = None
        self.__nodes = 0
