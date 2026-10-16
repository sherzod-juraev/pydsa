"""Doubly linked list.

Provides :class:`DoublyList`, a linked list whose nodes know both neighbours,
built on :class:`~pydsa.linear.base.LinkedListBase`.
"""

from collections.abc import Iterator
from typing import cast

from ..exc import IndexOutOfRangeError
from .base import LinkedListBase


class _DoublyNode[T]:
    """A node holding a value and links to both neighbours.

    Attributes
    ----------
    value : T
        The element stored in the node.
    next : _DoublyNode or None
        The following node, or ``None`` for the last node.
    prev : _DoublyNode or None
        The preceding node, or ``None`` for the first node.
    """

    def __init__(self, value: T) -> None:
        """Create a node holding ``value`` with no neighbours."""
        self.value: T = value
        self.next: _DoublyNode[T] | None = None
        self.prev: _DoublyNode[T] | None = None


class DoublyList[T](LinkedListBase[T, _DoublyNode[T]]):
    """A doubly linked list with head and tail pointers.

    Every node knows both neighbours, so both ends can be added to and removed from
    in constant time, and an indexed access walks from whichever end is closer.
    Everything not listed below is inherited from
    :class:`~pydsa.linear.base.LinkedListBase`.

    Time Complexity Summary

    .. csv-table:: DoublyList Operations Complexity
       :header: "Operation", "Time"
       :widths: 30, 15

       "insert_first, insert_last", "O(1)"
       "insert_at", "O(n)"
       "remove_first, remove_last", "O(1)"
       "remove_at", "O(n)"
       "reverse, __reversed__", "O(n)"

    *n = number of elements. Positional operations take at most n / 2 steps.*

    Examples
    --------
    >>> items = DoublyList[int]()
    >>> for value in (1, 2, 3):
    ...     items.insert_last(value)
    >>> list(reversed(items))
    [3, 2, 1]
    >>> items.remove_last(), list(items)
    (3, [1, 2])
    """

    def _node_at(self, index: int, /) -> _DoublyNode[T]:
        """Walk to the node at ``index`` from whichever end is closer.

        O(min(index, n - 1 - index)), so at most about n / 2 steps.
        """
        if index <= self._length // 2:
            current = cast(_DoublyNode[T], self._head)
            for _ in range(index):
                current = cast(_DoublyNode[T], current.next)
            return current
        current = cast(_DoublyNode[T], self._tail)
        for _ in range(self._length - 1 - index):
            current = cast(_DoublyNode[T], current.prev)
        return current

    def __reversed__(self) -> Iterator[T]:
        """Iterate over the values from the last element to the first. O(n).

        Yields
        ------
        T
            Each stored value, in reverse list order.

        Examples
        --------
        >>> items = DoublyList[str]()
        >>> for value in ("a", "b", "c"):
        ...     items.insert_last(value)
        >>> list(reversed(items))
        ['c', 'b', 'a']
        """
        current = self._tail
        while current:
            yield current.value
            current = cast(_DoublyNode[T], current.prev)

    def insert_first(self, value: T, /) -> None:
        """Insert ``value`` at the front of the list. O(1).

        Parameters
        ----------
        value : T
            The value to insert.
        """
        new_node = _DoublyNode(value)
        if not self:
            self._head = self._tail = new_node
        else:
            head = cast(_DoublyNode[T], self._head)
            new_node.next = head
            head.prev = new_node
            self._head = new_node
        self._length += 1

    def insert_last(self, value: T, /) -> None:
        """Append ``value`` to the end of the list. O(1).

        Parameters
        ----------
        value : T
            The value to append.
        """
        if not self:
            return self.insert_first(value)
        new_node = _DoublyNode(value)
        tail = cast(_DoublyNode[T], self._tail)
        new_node.prev = tail
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
        if index == self._length:
            return self.insert_last(value)
        current = self._node_at(index)
        new_node = _DoublyNode(value)
        new_node.next = current
        new_node.prev = current.prev
        if current.prev is not None:
            current.prev.next = new_node
        current.prev = new_node
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
        head = cast(_DoublyNode[T], self._head)
        self._head = head.next
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        head.next = None
        self._length -= 1
        return head.value

    def remove_last(self) -> T:
        """Remove and return the last element. O(1).

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
        tail = cast(_DoublyNode[T], self._tail)
        new_tail = cast(_DoublyNode[T], tail.prev)
        new_tail.next = None
        tail.prev = None
        self._tail = new_tail
        self._length -= 1
        return tail.value

    def remove_at(self, index: int, /) -> T:
        """Remove and return the element at ``index``. O(n).

        Finding the node takes at most n / 2 steps; unlinking it is O(1).

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
        if index == self._length - 1:
            return self.remove_last()
        current = self._node_at(index)
        prev = cast(_DoublyNode[T], current.prev)
        next = cast(_DoublyNode[T], current.next)
        prev.next = next
        next.prev = prev
        current.next, current.prev = None, None
        self._length -= 1
        return current.value

    def reverse(self) -> None:
        """Reverse the list in place by swapping the links of every node. O(n).

        Head and tail swap roles.
        """
        if self._length <= 1:
            return
        current = self._head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self._head, self._tail = self._tail, self._head
