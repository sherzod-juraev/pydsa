from typing import TypeVar, cast

from ..exc import EmptyError
from .singly.node import Node

T = TypeVar("T")


class Queue[T]:
    """
    A first-in, first-out (FIFO) queue implemented with a singly linked list.

    Elements are enqueued at the tail and dequeued from the head,
    giving O(1) time for both operations. A tail pointer is
    maintained to avoid traversing the list on each enqueue.

    .. csv-table:: Queue Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 10, 10

       "enqueue", "O(1)", "O(1)"
       "dequeue", "O(1)", "O(1)"
       "peek", "O(1)", "O(1)"
       "is_empty", "O(1)", "O(1)"
       "__len__", "O(1)", "O(1)"

    Notes
    -----
    This queue adapter restricts a singly linked list to FIFO
    operations. The underlying list uses both head and tail
    pointers to achieve constant-time insertion at the rear.
    """

    def __init__(self) -> None:

        self.__head: Node[T] | None = None
        self.__tail: Node[T] | None = None
        self.__length = 0

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return self.__length

    def is_empty(self) -> bool:
        """Return True if the queue is empty. O(1)."""
        return self.__length == 0

    def __bool__(self) -> bool:
        return not self.is_empty()

    def peek(self) -> T:
        """Return the front element without removing it. O(1).

        Raises
        ------
        EmptyError
            If the queue is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        head = cast(Node[T], self.__head)
        return head.value

    def enqueue(self, value: T, /) -> None:
        """Add a value to the rear of the queue. O(1)."""
        new_node = Node(value)
        if self.is_empty():
            self.__head = new_node
            self.__tail = new_node
        else:
            tail = cast(Node[T], self.__tail)
            tail.next = new_node
            self.__tail = new_node
        self.__length += 1

    def dequeue(self) -> T:
        """Remove and return the front element. O(1).

        Raises
        ------
        EmptyError
            If the queue is empty.
        """
        if self.is_empty():
            raise EmptyError(self)
        head = cast(Node[T], self.__head)
        current = head
        self.__head = head.next
        if self.__head is None:
            self.__tail = None
        current.next = None
        self.__length -= 1
        return current.value
