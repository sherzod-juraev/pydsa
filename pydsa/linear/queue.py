"""First-in, first-out queue.

Provides :class:`Queue`, a thin wrapper around
:class:`~pydsa.linear.singly.SinglyList` that exposes only enqueue, dequeue and
peek.
"""

from ..core import BaseStructure
from .singly import SinglyList


class Queue[T](BaseStructure):
    """A first-in, first-out (FIFO) queue.

    Values leave in the order they arrived. The queue is backed by a
    :class:`~pydsa.linear.singly.SinglyList`: values are added at the tail and
    removed from the head, both in constant time. Only the queue operations are
    exposed, so the order cannot be broken from outside.

    Time Complexity Summary

    .. csv-table:: Queue Operations Complexity
       :header: "Operation", "Time"
       :widths: 30, 15

       "enqueue", "O(1)"
       "dequeue", "O(1)"
       "peek", "O(1)"
       "clear", "O(1)"
       "__len__", "O(1)"

    Notes
    -----
    - An empty queue is falsy and a non-empty one is truthy.

    Examples
    --------
    >>> queue = Queue[int]()
    >>> queue.enqueue(1)
    >>> queue.enqueue(2)
    >>> queue.peek()
    1
    >>> queue.dequeue(), queue.dequeue()
    (1, 2)
    >>> bool(queue)
    False
    """

    def __init__(self) -> None:
        """Create an empty queue."""
        self._items: SinglyList[T] = SinglyList[T]()

    def __len__(self) -> int:
        """Return the number of values in the queue. O(1)."""
        return len(self._items)

    def enqueue(self, value: T, /) -> None:
        """Add ``value`` at the back of the queue. O(1).

        Parameters
        ----------
        value : T
            The value to add.
        """
        self._items.insert_last(value)

    def dequeue(self) -> T:
        """Remove and return the value at the front. O(1).

        Returns
        -------
        T
            The value that has waited longest.

        Raises
        ------
        EmptyError
            If the queue is empty.
        """
        self._ensure_not_empty()
        return self._items.remove_first()

    def peek(self) -> T:
        """Return the value at the front without removing it. O(1).

        Returns
        -------
        T
            The value that has waited longest.

        Raises
        ------
        EmptyError
            If the queue is empty.
        """
        self._ensure_not_empty()
        return self._items[0]

    def clear(self) -> None:
        """Remove every value from the queue. O(1)."""
        self._items.clear()
