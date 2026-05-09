from .singly.node import Node
from typing import Any
from ..exc import Empty


class Stack:
    """
    A last-in, first-out (LIFO) stack implemented with a singly linked list.

    All core operations run in O(1) time using head-insertion and
    head-removal, ensuring constant-time push, pop, and peek.

    Time Complexity
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

        self.__head: Node | None = None
        self.__length: int = 0

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return self.__length

    def is_empty(self) -> bool:
        """Return True if the stack is empty. O(1)."""
        return self.__length == 0

    def peek(self) -> Any:
        """Return the top element without removing it. O(1).

        Raises
        ------
        Empty
            If the stack is empty.
        """
        if self.is_empty():
            raise Empty(self)
        return self.__head.value

    def pop(self) -> Any:
        """Remove and return the top element. O(1).

        Raises
        ------
        Empty
            If the stack is empty.
        """
        if self.is_empty():
            raise Empty(self)
        current = self.__head
        self.__head = self.__head.next
        current.next = None
        self.__length -= 1
        return current.value

    def push(self, value: Any, /) -> None:
        """Push a value onto the top of the stack. O(1)."""
        new_node = Node(value)
        new_node.next = self.__head
        self.__head = new_node
        self.__length += 1