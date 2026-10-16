"""Singly linked list.

Provides :class:`SinglyList`, a linked list whose nodes know only their
successor, built on :class:`~pydsa.linear.base.LinkedListBase`.
"""

from typing import cast

from ..exc import IndexOutOfRangeError
from .base import LinkedListBase


class _Node[T]:
    """A node holding a value and a link to the next node.

    Attributes
    ----------
    value : T
        The element stored in the node.
    next : _Node or None
        The following node, or ``None`` for the last node.
    """

    def __init__(self, value: T) -> None:
        """Create a node holding ``value`` with no successor."""
        self.value: T = value
        self.next: _Node[T] | None = None


class SinglyList[T](LinkedListBase[T, _Node[T]]):
    """A singly linked list with head and tail pointers.

    Every node knows only its successor. The tail pointer makes appending as cheap
    as prepending, but removing the last element still has to walk from the head to
    find its predecessor. Everything not listed below is inherited from
    :class:`~pydsa.linear.base.LinkedListBase`.

    Time Complexity Summary

    .. csv-table:: SinglyList Operations Complexity
       :header: "Operation", "Time"
       :widths: 30, 15

       "insert_first", "O(1)"
       "insert_last", "O(1)"
       "insert_at", "O(n)"
       "remove_first", "O(1)"
       "remove_last", "O(n)"
       "remove_at", "O(n)"
       "reverse", "O(n)"

    *n = number of elements.*

    Examples
    --------
    >>> items = SinglyList[int]()
    >>> items.insert_first(2)
    >>> items.insert_first(1)
    >>> items.insert_last(3)
    >>> list(items)
    [1, 2, 3]
    >>> items.remove_last()
    3
    >>> list(items)
    [1, 2]
    """

    def _node_at(self, index: int, /) -> _Node[T]:
        """Walk from the head to the node at ``index``. O(index)."""
        current = cast(_Node[T], self._head)
        for _ in range(index):
            current = cast(_Node[T], current.next)
        return current

    def insert_first(self, value: T, /) -> None:
        """Insert ``value`` at the front of the list. O(1).

        Parameters
        ----------
        value : T
            The value to insert.
        """
        new_node = _Node(value)
        new_node.next = self._head
        self._head = new_node
        if self._tail is None:
            self._tail = new_node
        self._length += 1

    def insert_last(self, value: T, /) -> None:
        """Append ``value`` to the end of the list. O(1).

        The tail pointer is used, so no walk is needed.

        Parameters
        ----------
        value : T
            The value to append.
        """
        if not self:
            return self.insert_first(value)
        new_node = _Node[T](value)
        tail = cast(_Node[T], self._tail)
        tail.next = new_node
        self._tail = new_node
        self._length += 1

    def insert_at(self, index: int, value: T, /) -> None:
        """Insert ``value`` so that it ends up at position ``index``. O(n).

        Positions ``0 .. len`` are valid and a negative index is shifted by the
        length first.

        Parameters
        ----------
        index : int
            Target position, in ``-len .. len``.
        value : T
            The value to insert.

        Raises
        ------
        IndexOutOfRangeError
            If ``index`` is outside ``-len .. len``.
        """
        if index < 0:
            index += self._length
        if index < 0 or index > self._length:
            raise IndexOutOfRangeError(
                f"{type(self).__name__} index {index} out of range for length {self._length}"
            )
        if index == 0:
            return self.insert_first(value)
        elif index == self._length:
            return self.insert_last(value)
        current = cast(_Node[T], self._head)
        for _ in range(index - 1):
            current = cast(_Node[T], current.next)
        new_node = _Node(value)
        new_node.next = current.next
        current.next = new_node
        self._length += 1

    def remove_first(self) -> T:
        """Remove and return the first element. O(1).

        Returns
        -------
        T
            The removed value.

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        self._ensure_not_empty()
        current = cast(_Node[T], self._head)
        self._head = current.next
        if self._head is None:
            self._tail = None
        self._length -= 1
        return current.value

    def remove_last(self) -> T:
        """Remove and return the last element. O(n).

        Singly linked nodes cannot reach their predecessor, so the walk starts at the
        head.

        Returns
        -------
        T
            The removed value.

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        self._ensure_not_empty()
        if self._length == 1:
            return self.remove_first()
        current = cast(_Node[T], self._head)
        while current is not None and current.next != self._tail:
            current = cast(_Node[T], current.next)
        last_node = cast(_Node[T], self._tail)
        current.next = None
        self._tail = current
        self._length -= 1
        return last_node.value

    def remove_at(self, index: int, /) -> T:
        """Remove and return the element at ``index``. O(n).

        Parameters
        ----------
        index : int
            Position of the element, in ``-len .. len - 1``.

        Returns
        -------
        T
            The removed value.

        Raises
        ------
        IndexOutOfRangeError
            If ``index`` is outside ``-len .. len - 1``.
        """
        index = self._normalize_index(index)
        if index == 0:
            return self.remove_first()
        elif index == self._length - 1:
            return self.remove_last()
        current = cast(_Node[T], self._head)
        for _ in range(index - 1):
            current = cast(_Node[T], current.next)
        remove_node = cast(_Node[T], current.next)
        current.next = remove_node.next
        remove_node.next = None
        self._length -= 1
        return remove_node.value

    def reverse(self) -> None:
        """Reverse the list in place by flipping every link. O(n).

        Head and tail swap roles.
        """
        old_head = self._head
        prev = None
        current = self._head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self._head = prev
        self._tail = old_head
