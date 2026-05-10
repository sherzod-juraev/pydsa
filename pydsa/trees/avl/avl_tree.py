from .node import Node
from typing import Any, Iterator
from ...exc import Empty
from ...linear import Stack, Queue


class AVLTree:
    """
    A self-balancing binary search tree (AVL) where the height
    difference between left and right subtrees of any node is at most 1.

    After every insertion and deletion, balance factors are checked
    and rotations (LL, RR, LR, RL) are applied to restore the invariant.
    This guarantees O(log n) height and O(log n) search, insert, and
    remove operations in both average and worst cases.

    Time Complexity
    .. csv-table:: AVL Tree Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "insert", "O(log n)", "O(log n)"
       "remove", "O(log n)", "O(log n)"
       "search", "O(log n)", "O(1)"
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

        self.__root: Node | None = None
        self.__nodes: int = 0

    def __len__(self) -> int:
        """Return the number of nodes. O(1)."""
        return self.__nodes

    def __bool__(self) -> bool:
        """Return True if the tree is not empty. O(1)."""
        return self.__nodes > 0

    def __contains__(self, item) -> bool:
        """Return True if the value exists in the tree. O(log n)."""
        current: Node = self.__root
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

    def root(self) -> Any:
        """Return the value of the root node. O(1).

        Raises
        ------
        Empty
            If the tree is empty.
        """
        if self.is_empty():
            raise Empty(self)
        return self.__root.value

    def insert(self, value: Any, /) -> None:
        """Insert a value and rebalance the tree. O(log n).

        Duplicate values are silently ignored. The AVL invariant
        is restored after insertion via rotations if necessary.

        Parameters
        ----------
        value : Any
            The value to insert.
        """
        if self.is_empty():
            self.__root = Node(value)
            self.__nodes += 1
            return
        stack = Stack()
        current: Node = self.__root
        while current:
            if current.value == value:
                return
            stack.push(current)
            if current.value < value:
                current = current.right
            else:
                current = current.left
        parent: Node = stack.peek()
        new_node = Node(value)
        if parent.value < value:
            parent.right = new_node
        else:
            parent.left = new_node
        self.__nodes += 1
        while stack:
            node: Node = stack.pop()
            node_balanced = self.__get_balance(node)
            if stack.is_empty():
                self.__root = node_balanced
            else:
                parent: Node = stack.peek()
                if parent.value < node_balanced.value:
                    parent.right = node_balanced
                else:
                    parent.left = node_balanced

    def remove(self, value: Any, /) -> None:
        """Remove a value and rebalance the tree. O(log n).

        Handles the three standard BST removal cases (leaf, one child,
        two children) and applies rotations on the path back to the
        root to maintain the AVL invariant.

        If the value is not found, the tree is unchanged.

        Parameters
        ----------
        value : Any
            The value to remove.
        """
        if self.is_empty():
            return
        stack = Stack()
        current = self.__root
        while current and current.value != value:
            stack.push(current)
            current = current.left if value < current.value else current.right
        if not current: return
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

    def __get_height(self, node: Node | None, /) -> int:
        """Return the height of a node, treating None as 0."""
        return node.height if node else 0

    def __update_height(self, node: Node, /) -> None:
        """Update the height of a node based on its children."""
        node.height = 1 + max(
            self.__get_height(node.left), self.__get_height(node.right)
        )

    def __get_balance(self, node: Node, /) -> Node:
        """Update height and apply rotation if the node is unbalanced.

        Returns
        -------
        Node
            The new root of the subtree after balancing.
        """
        self.__update_height(node)
        bf = self.__get_height(node.left) - self.__get_height(node.right)
        if bf > 1:
            if self.__get_height(node.left.right) > self.__get_height(node.left.left):
                node.left = self.__left_rotate(node.left)
            return self.__right_rotate(node)
        elif bf < -1:
            if self.__get_height(node.right.left) > self.__get_height(node.right.right):
                node.right = self.__right_rotate(node.right)
            return self.__left_rotate(node)
        return node

    def __right_rotate(self, node: Node, /) -> Node:
        """Perform a right rotation (LL case).

        Returns
        -------
        Node
            The new root after rotation.
        """
        left_tree = node.left
        T2 = left_tree.right
        left_tree.right = node
        node.left = T2
        self.__update_height(node)
        self.__update_height(left_tree)
        return left_tree

    def __left_rotate(self, node: Node, /) -> Node:
        """Perform a left rotation (RR case).

        Returns
        -------
        Node
            The new root after rotation.
        """
        right_tree = node.right
        T2 = right_tree.left
        right_tree.left = node
        node.right = T2
        self.__update_height(node)
        self.__update_height(right_tree)
        return right_tree

    def search(self, value: Any, /) -> bool:
        """Return True if the value exists in the tree. O(log n)."""
        return value in self

    def min_value(self) -> Any:
        """Return the minimum value in the tree (leftmost node). O(log n).

        Raises
        ------
        Empty
            If the tree is empty.
        """
        if self.is_empty():
            raise Empty(self)
        current = self.__root
        while current.left:
            current = current.left
        return current.value

    def max_value(self) -> Any:
        """Return the maximum value in the tree (rightmost node). O(log n).

        Raises
        ------
        Empty
            If the tree is empty.
        """
        if self.is_empty():
            raise Empty(self)
        current = self.__root
        while current.right:
            current = current.right
        return current.value

    def preorder(self) -> Iterator:
        """Yield values in preorder traversal (root → left → right). O(n)."""
        if self.is_empty():
            return
        stack = Stack()
        stack.push(self.__root)
        while stack:
            current: Node = stack.pop()
            yield current.value
            if current.right:
                stack.push(current.right)
            if current.left:
                stack.push(current.left)

    def inorder(self) -> Iterator:
        """Yield values in inorder traversal (left → root → right). O(n).

        Because this is a BST, values are yielded in sorted ascending order.
        """
        if self.is_empty():
            return
        stack = Stack()
        current = self.__root
        while stack or current:
            while current:
                stack.push(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def postorder(self) -> Iterator:
        """Yield values in postorder traversal (left → right → root). O(n)."""
        if self.is_empty():
            return
        stack = Stack()
        current: Node | None = self.__root
        last_visited: Node | None = None
        while stack or current:
            if current:
                stack.push(current)
                current = current.left
            else:
                peek_node: Node = stack.peek()
                if peek_node.right and peek_node.right != last_visited:
                    current = peek_node.right
                else:
                    last_visited = stack.pop()
                    yield last_visited.value
                    current = None

    def levelorder(self) -> Iterator:
        """Yield values in level-order (BFS) traversal. O(n)."""
        if self.is_empty():
            return
        queue = Queue()
        queue.enqueue(self.__root)
        while queue:
            current: Node = queue.dequeue()
            yield current.value
            if current.left:
                queue.enqueue(current.left)
            if current.right:
                queue.enqueue(current.right)

    def height(self) -> int:
        """Return the height of the tree. O(1).

        A single-node tree has height 1. Empty tree has height 0.
        """
        if self.is_empty():
            return 0
        return self.__root.height

    def clear(self) -> None:
        """Remove all nodes from the tree. O(1)."""
        self.__root = None
        self.__nodes = 0