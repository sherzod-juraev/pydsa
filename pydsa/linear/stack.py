"""Last-in, first-out stack.

Provides :class:`Stack`, a thin wrapper around
:class:`~pydsa.linear.singly.SinglyList` that exposes only push, pop and peek.
"""

from ..core import BaseStructure
from .singly import SinglyList


class Stack[T](BaseStructure):
    """A last-in, first-out (LIFO) stack.

    The most recently pushed value is the first one popped. The stack is backed by
    a :class:`~pydsa.linear.singly.SinglyList` whose front is the top, and only the
    stack operations are exposed, so the order cannot be broken from outside.

    Time Complexity Summary

    .. csv-table:: Stack Operations Complexity
       :header: "Operation", "Time"
       :widths: 30, 15

       "push", "O(1)"
       "pop", "O(1)"
       "peek", "O(1)"
       "clear", "O(1)"
       "__len__", "O(1)"

    Notes
    -----
    - An empty stack is falsy and a non-empty one is truthy.

    Examples
    --------
    >>> stack = Stack[int]()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> stack.peek()
    2
    >>> stack.pop(), stack.pop()
    (2, 1)
    >>> bool(stack)
    False
    """

    def __init__(self) -> None:
        """Create an empty stack."""
        self._items: SinglyList[T] = SinglyList[T]()

    def __len__(self) -> int:
        """Return the number of values on the stack. O(1)."""
        return len(self._items)

    def push(self, value: T, /) -> None:
        """Put ``value`` on top of the stack. O(1).

        Parameters
        ----------
        value : T
            The value to push.
        """
        self._items.insert_first(value)

    def pop(self) -> T:
        """Remove and return the top value. O(1).

        Returns
        -------
        T
            The most recently pushed value still on the stack.

        Raises
        ------
        EmptyError
            If the stack is empty.
        """
        self._ensure_not_empty()
        return self._items.remove_first()

    def peek(self) -> T:
        """Return the top value without removing it. O(1).

        Returns
        -------
        T
            The most recently pushed value still on the stack.

        Raises
        ------
        EmptyError
            If the stack is empty.
        """
        self._ensure_not_empty()
        return self._items[0]

    def clear(self) -> None:
        """Remove every value from the stack. O(1)."""
        self._items.clear()
