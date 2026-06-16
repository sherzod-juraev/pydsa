from collections.abc import Iterator
from typing import cast

from ..._types import Comparable
from ...exc import EmptyError
from ...linear import Queue, Stack
from .node import Node


class AVLTree[T: Comparable]:
    """
    A self-balancing binary searching tree (AVL) where the height
    difference between left and right subtrees of T node is at most 1.

    After every insertion and deletion, balance factors are checked
    and rotations (LL, RR, LR, RL) are applied to restore the invariant.
    This guarantees O(log n) height and O(log n) searching, insert, and
    remove operations in both average and worst cases.

    Time Complexity
    .. csv-table:: AVL Tree Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "insert", "O(log n)", "O(log n)"
       "remove", "O(log n)", "O(log n)"
       "searching", "O(log n)", "O(1)"
       "min_value", "O(log n)", "O(1)"
       "max_value", "O(log n)", "O(1)"
       "preorder", "O(n)", "O(h)"
       "inorder", "O(n)", "O(h)"
       "postorder", "O(n)", "O(h)"
       "levelorder", "O(n)", "O(w)"
       "height", "O(1)", "O(1)"
       "__contains__", "O(log n)", "O(1)"

    *h = height (O(log n)), w = maximum width*

    Notes
    -----
    - Balance factor: ``bf = height(left) - height(right)``.
    - Invariant: ``|bf| ≤ 1`` for every node.
    - Rotations: Right (LL, LR), Left (RR, RL).
    - All traversals are iterative using custom Stack and Queue ADTs.
    - Duplicate values are silently ignored.
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
        """Return True if the value exists in the tree. O(log n)."""
        current = self.__root
        while current:
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
        """Insert a value and rebalance the tree. O(log n).

        Duplicate values are silently ignored. The AVL invariant
        is restored after insertion via rotations if necessary.

        Parameters
        ----------
        value : T
            The value to insert.
        """
        if self.is_empty():
            self.__root = Node(value)
            self.__nodes += 1
            return
        stack: Stack[Node[T]] = Stack()
        current = self.__root
        while current is not None:
            if current.value == value:
                return
            stack.push(current)
            current = current.right if current.value < value else current.left
        parent: Node[T] = stack.peek()
        new_node = Node(value)
        if parent.value < value:
            parent.right = new_node
        else:
            parent.left = new_node
        self.__nodes += 1
        while stack:
            node: Node[T] = stack.pop()
            node_balanced = self.__get_balance(node)
            if stack.is_empty():
                self.__root = node_balanced
            else:
                parent = stack.peek()
                if parent.value < node_balanced.value:
                    parent.right = node_balanced
                else:
                    parent.left = node_balanced

    def remove(self, value: T, /) -> None:
        """Remove a value and rebalance the tree. O(log n).

        Handles the three standard BST removal cases (leaf, one child,
        two children) and applies rotations on the path back to the
        root to maintain the AVL invariant.

        If the value is not found, the tree is unchanged.

        Parameters
        ----------
        value : T
            The value to remove.
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        current = self.__root
        while current is not None and current.value != value:
            stack.push(current)
            current = current.left if value < current.value else current.right
        if not current:
            return
        if current.left and current.right:
            stack.push(current)
            successor = current.right
            while successor.left:
                stack.push(successor)
                successor = successor.left
            current.value = successor.value
            current = successor
        child = current.left if current.left else current.right
        if not stack:
            self.__root = child
        else:
            parent = stack.peek()
            if current is parent.left:
                parent.left = child
            else:
                parent.right = child
        while stack:
            node = stack.pop()
            balanced_node = self.__get_balance(node)
            if not stack:
                self.__root = balanced_node
            else:
                parent = stack.peek()
                if node is parent.left:
                    parent.left = balanced_node
                else:
                    parent.right = balanced_node
        self.__nodes -= 1

    def __get_height(self, node: Node[T] | None, /) -> int:
        """Return the height of a node, treating None as 0."""
        return node.height if node is not None else 0

    def __update_height(self, node: Node[T], /) -> None:
        """Update the height of a node based on its children."""
        node.height = 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def __get_balance(self, node: Node[T], /) -> Node[T]:
        """Update height and apply rotation if the node is unbalanced.

        Returns
        -------
        Node
            The new root of the subtree after balancing.
        """
        self.__update_height(node)
        bf = self.__get_height(node.left) - self.__get_height(node.right)
        if bf > 1:
            left = cast(Node[T], node.left)
            if self.__get_height(left.right) > self.__get_height(left.left):
                node.left = self.__left_rotate(left)
            return self.__right_rotate(node)
        elif bf < -1:
            right = cast(Node[T], node.right)
            if self.__get_height(right.left) > self.__get_height(right.right):
                node.right = self.__right_rotate(right)
            return self.__left_rotate(node)
        return node

    def __right_rotate(self, node: Node[T], /) -> Node[T]:
        """Perform a right rotation (LL case).

        Returns
        -------
        Node
            The new root after rotation.
        """
        left_tree = cast(Node[T], node.left)
        t2 = left_tree.right
        left_tree.right = node
        node.left = t2
        self.__update_height(node)
        self.__update_height(left_tree)
        return left_tree

    def __left_rotate(self, node: Node[T], /) -> Node[T]:
        """Perform a left rotation (RR case).

        Returns
        -------
        Node
            The new root after rotation.
        """
        right_tree = cast(Node[T], node.right)
        t2 = right_tree.left
        right_tree.left = node
        node.right = t2
        self.__update_height(node)
        self.__update_height(right_tree)
        return right_tree

    def search(self, value: T, /) -> bool:
        """Return True if the value exists in the tree. O(log n)."""
        return value in self

    def min_value(self) -> T:
        """Return the minimum value in the tree (leftmost node). O(log n).

        Raises
        ------
        EmptyError
            If the tree is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        current = cast(Node[T], self.__root)
        while current.left is not None:
            current = current.left
        return current.value

    def max_value(self) -> T:
        """Return the maximum value in the tree (rightmost node). O(log n).

        Raises
        ------
        EmptyError
            If the tree is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        current = cast(Node[T], self.__root)
        while current.right is not None:
            current = current.right
        return current.value

    def preorder(self) -> Iterator[T]:
        """Yield values in preorder traversal (root → left → right). O(n)."""
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        stack.push(cast(Node[T], self.__root))
        while stack:
            current: Node[T] = stack.pop()
            yield current.value
            if current.right is not None:
                stack.push(current.right)
            if current.left is not None:
                stack.push(current.left)

    def inorder(self) -> Iterator[T]:
        """Yield values in inorder traversal (left → root → right). O(n).

        Because this is a BST, values are yielded in sorted ascending order.
        """
        if self.is_empty():
            return
        stack: Stack[Node[T]] = Stack()
        current: Node[T] | None = cast(Node[T], self.__root)
        while stack or current is not None:
            while current is not None:
                stack.push(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def postorder(self) -> Iterator[T]:
        """Yield values in postorder traversal (left → right → root). O(n)."""
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
        """Yield values in level-order (BFS) traversal. O(n)."""
        if self.is_empty():
            return
        queue: Queue[Node[T]] = Queue()
        queue.enqueue(cast(Node[T], self.__root))
        while queue:
            current: Node[T] = queue.dequeue()
            yield current.value
            if current.left is not None:
                queue.enqueue(current.left)
            if current.right is not None:
                queue.enqueue(current.right)

    def height(self) -> int:
        """Return the height of the tree. O(1).

        A single-node tree has height 1. Empty tree has height 0.
        """
        if self.is_empty():
            return 0
        root = cast(Node[T], self.__root)
        return root.height

    def clear(self) -> None:
        """Remove all nodes from the tree. O(1)."""
        self.__root = None
        self.__nodes = 0
