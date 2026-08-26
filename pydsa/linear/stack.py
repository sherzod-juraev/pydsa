"""Stack (LIFO) implementation.

Provides :class:`Stack`, a last-in-first-out stack built as a thin
adapter over :class:`~pydsa.linear.singly.node.Node`, restricting
access to push, pop, and peek at the head.
"""

from typing import cast

from ..exc import EmptyError
from .singly.node import Node


class Stack[T]:
    """
    A last-in, first-out (LIFO) stack implemented with a singly linked list.

    All core operations run in O(1) time using head-insertion and
    head-removal, ensuring constant-time push, pop, and peek.

    Time Complexity Summary

    .. csv-table:: Stack Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "push", "O(1)", "O(1)"
       "pop", "O(1)", "O(1)"
       "peek", "O(1)", "O(1)"
       "is_empty", "O(1)", "O(1)"
       "__len__", "O(1)", "O(1)"

    Notes
    -----
    This is an adapter over a singly linked list, restricting the
    interface to LIFO operations. The underlying list is managed
    without a tail pointer since only the head is mutated.
    """

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self.__head: Node[T] | None = None
        self.__length: int = 0

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return self.__length

    def is_empty(self) -> bool:
        """Return True if the stack is empty. O(1)."""
        return self.__length == 0

    def __bool__(self) -> bool:
        """Return True if the stack is not empty. O(1)."""
        return not self.is_empty()

    def push(self, value: T, /) -> None:
        """Push a value onto the top of the stack. O(1).

        Examples
        --------
        >>> s = Stack[int]()
        >>> s.push(1)
        >>> s.peek()
        1
        """
        new_node = Node(value)
        new_node.next = self.__head
        self.__head = new_node
        self.__length += 1

    def pop(self) -> T:
        """Remove and return the top element. O(1).

        Raises
        ------
        EmptyError
            If the stack is empty.

        Examples
        --------
        >>> s = Stack[int]()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.pop()
        2
        """
        if self.is_empty():
            raise EmptyError(self)
        head = cast(Node[T], self.__head)
        current = head
        self.__head = head.next
        current.next = None
        self.__length -= 1
        return current.value

    def peek(self) -> T:
        """Return the top element without removing it. O(1).

        Raises
        ------
        EmptyError
            If the stack is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        head = cast(Node[T], self.__head)
        return head.value
