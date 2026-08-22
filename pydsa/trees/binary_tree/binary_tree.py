"""General binary tree implementation.

Provides :class:`BinaryTree`, a general binary tree with path-based
insertion and four traversal strategies (preorder, inorder, postorder,
level-order).
"""

from collections.abc import Iterator
from typing import cast

from ...exc import EmptyError
from ...linear import Queue, Stack
from .node import Node


class BinaryTree[T]:
    """
    A general binary tree with path-based insertion and four traversal strategies.

    Nodes are inserted by specifying a path string (e.g., ``"LLR"``)
    from the root. The tree supports preorder, inorder, postorder
    (all iterative, O(n) time, O(h) space), and level-order (BFS,
    O(n) time, O(w) space) traversal.

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
       "is_empty", "O(1)", "O(1)"
       "__len__", "O(1)", "O(1)"
       "clear", "O(1)", "O(1)"

    *h = height, w = maximum width of the tree*

    Notes
    -----
    This is a general binary tree without ordering constraints.
    For a binary searching tree (BST) with the ``left < root < right``
    invariant, see the ``BSTree`` class.
    """

    def __init__(self) -> None:
        """Initialize an empty tree."""
        self.__root: Node[T] | None = None
        self.__nodes: int = 0

    def __len__(self) -> int:
        """Return the number of nodes. O(1)."""
        return self.__nodes

    def __bool__(self) -> bool:
        """Return True if the tree is not empty. O(1)."""
        return self.__nodes > 0

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

    def insert(self, value: T, path: str, /) -> None:
        """Insert a value at the node specified by a path string. O(h).

        The path is a sequence of ``'L'`` and ``'R'`` characters
        starting from the root. An empty path always targets the
        root — if the tree is non-empty, the new node replaces the
        root while preserving its existing subtree. If a node already
        exists at a non-root path, its subtree is preserved as the
        subtree of the new node.

        Parameters
        ----------
        value : Any
            The value to insert.
        path : str
            Path from root, e.g., ``"LLR"`` means left, left, right.
            Empty string targets the root.

        Raises
        ------
        ValueError
            If the path cannot be traversed because an intermediate
            node is missing.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        """
        new_node = Node(value)
        if not path:
            new_node.left = self.__root.left if self.__root is not None else None
            new_node.right = self.__root.right if self.__root is not None else None
            self.__root = new_node
            self.__nodes += 1
            return
        if self.is_empty():
            raise ValueError(f"Path is broken: {path} does not exist")
        current = cast(Node[T], self.__root)
        for i in range(len(path) - 1):
            if path[i] == "L":
                if current.left is None:
                    raise ValueError(f"Path is broken: {path} does not exist")
                current = current.left
            elif path[i] == "R":
                if current.right is None:
                    raise ValueError(f"Path is broken: {path} does not exist")
                current = current.right
        if path[-1] == "L":
            new_node.left = current.left
            current.left = new_node
        elif path[-1] == "R":
            new_node.right = current.right
            current.right = new_node
        self.__nodes += 1

    def preorder(self) -> Iterator[T]:
        """Yield values in preorder traversal (root → left → right). O(n).

        Uses an explicit stack to simulate recursion.

        Returns
        -------
        Iterator
            Values in preorder sequence.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> list(tree.preorder())
        [5, 3, 1, 8]
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        stack.push(cast(Node[T], self.__root))
        while stack:
            node: Node[T] = stack.pop()
            yield node.value
            if node.right:
                stack.push(node.right)
            if node.left:
                stack.push(node.left)

    def inorder(self) -> Iterator[T]:
        """Yield values in inorder traversal (left → root → right). O(n).

        Uses an explicit stack to simulate recursion.

        Returns
        -------
        Iterator
            Values in inorder sequence.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> list(tree.inorder())
        [1, 3, 5, 8]
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        current: Node[T] | None = self.__root
        while stack or current:
            while current:
                stack.push(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def postorder(self) -> Iterator[T]:
        """Yield values in postorder traversal (left → right → root). O(n).

        Uses an explicit stack and a ``last_visited`` marker to
        determine when the right subtree has been fully processed.

        Returns
        -------
        Iterator
            Values in postorder sequence.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> list(tree.postorder())
        [1, 3, 8, 5]
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        current = self.__root
        last_visited = None
        while stack or current:
            if current:
                stack.push(current)
                current = current.left
            else:
                peek_node: Node[T] = stack.peek()
                if peek_node.right and peek_node.right != last_visited:
                    current = peek_node.right
                else:
                    node: Node[T] = stack.pop()
                    yield node.value
                    last_visited = node
                    current = None

    def levelorder(self) -> Iterator[T]:
        """Yield values in level-order traversal (BFS, level by level). O(n).

        Uses an explicit queue to process nodes in breadth-first order.

        Returns
        -------
        Iterator
            Values in level-order sequence.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> list(tree.levelorder())
        [5, 3, 8, 1]
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
        """Return the height of the tree (number of nodes on the longest path).

        The longest path is measured from the root to a leaf. The operation
        takes O(n) time.

        A tree with a single node has height 1.

        Returns
        -------
        int
            Height in nodes.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> tree.height()
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

    def leaves(self) -> int:
        """Return the number of leaf nodes (nodes with no children). O(n).

        Returns
        -------
        int
            Leaf count.

        Examples
        --------
        >>> tree = BinaryTree()
        >>> tree.insert(5, "")
        >>> tree.insert(3, "L")
        >>> tree.insert(8, "R")
        >>> tree.insert(1, "LL")
        >>> tree.leaves()
        2
        """
        if self.is_empty():
            return 0
        count = 0
        queue: Queue[Node[T]] = Queue()
        queue.enqueue(cast(Node[T], self.__root))
        while queue:
            node: Node[T] = queue.dequeue()
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)
            if node.left is None and node.right is None:
                count += 1
        return count

    def clear(self) -> None:
        """Remove all nodes from the tree. O(1)."""
        self.__root = None
        self.__nodes = 0
