"""Shared foundation of the linked lists.

Provides :class:`LinkedListBase`, the abstract parent of
:class:`~pydsa.linear.singly.SinglyList` and
:class:`~pydsa.linear.doubly.DoublyList`. It owns the head, tail and length
bookkeeping and every operation that can be written without knowing how nodes
are linked; the subclasses supply only the pointer manipulation.
"""

from abc import abstractmethod
from collections.abc import Iterator
from typing import Any, Protocol, Self, cast

from ..core import BaseStructure
from ..exc import IndexOutOfRangeError


class _NodeProtocol[T](Protocol):
    """Structural type of a list node.

    A node carries a ``value`` and a ``next`` link to a node of the same kind, or
    ``None`` at the end of the chain. Any class with these two attributes can be
    used by :class:`LinkedListBase`.

    Attributes
    ----------
    value : T
        The element stored in the node.
    next : Self or None
        The following node, or ``None`` for the last node.
    """

    value: T
    next: Self | None


class LinkedListBase[T, NodeT: _NodeProtocol[Any]](BaseStructure):
    """Abstract base class of the linked lists.

    Keeps ``_head``, ``_tail`` and ``_length`` and implements, once, everything
    that only needs to walk the chain: iteration, indexing, searching, copying,
    ``remove(value)``, ``middle`` and ``has_cycle``. Subclasses provide the node
    type and the operations that change links: ``_node_at``, ``insert_first``,
    ``insert_last``, ``insert_at``, ``remove_first``, ``remove_last``,
    ``remove_at`` and ``reverse``.

    Time Complexity Summary

    .. csv-table:: Operations implemented in the base class
       :header: "Operation", "Time"
       :widths: 40, 15

       "__len__, get_first, get_last", "O(1)"
       "__getitem__, get_at", "O(n)"
       "__iter__, __contains__, index_of, count, remove", "O(n)"
       "copy, middle, has_cycle", "O(n)"
       "clear", "O(1)"

    *n = number of elements.*

    Notes
    -----
    - Indexes follow ``list``: a negative index counts from the end.
    - Values are compared with ``==``.
    - An empty list is falsy and a non-empty one is truthy.
    - Contract for subclasses: ``_head`` is the first node and ``_tail`` the last
      (both ``None`` when empty), ``_length`` is the number of nodes, and
      ``_node_at`` always receives an index already inside ``0 .. len - 1``.
    - Do not modify a list while iterating over it.

    Examples
    --------
    >>> from pydsa.linear import SinglyList
    >>> items = SinglyList[int]()
    >>> for value in (1, 2, 3):
    ...     items.insert_last(value)
    >>> list(items), len(items)
    ([1, 2, 3], 3)
    >>> items[-1], items.index_of(2), 3 in items
    (3, 1, True)
    """

    def __init__(self) -> None:
        """Create an empty list."""
        self._head: NodeT | None = None
        self._tail: NodeT | None = None
        self._length: int = 0

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return self._length

    def __iter__(self) -> Iterator[T]:
        """Iterate over the values from the first element to the last. O(n).

        Yields
        ------
        T
            Each stored value, in list order.
        """
        current = self._head
        while current:
            value: T = current.value
            yield value
            current = current.next

    def __getitem__(self, item: int) -> T:
        """Return the value at ``item``. O(n).

        A negative index counts from the end. The doubly linked list walks from
        whichever end is closer.

        Parameters
        ----------
        item : int
            Position of the element, in ``-len .. len - 1``.

        Returns
        -------
        T
            The value at that position.

        Raises
        ------
        IndexOutOfRangeError
            If ``item`` is outside ``-len .. len - 1``.

        Examples
        --------
        >>> from pydsa.linear import SinglyList
        >>> items = SinglyList[str]()
        >>> for value in ("a", "b", "c"):
        ...     items.insert_last(value)
        >>> items[0], items[-1]
        ('a', 'c')
        """
        item = self._normalize_index(item)
        value: T = self._node_at(item).value
        return value

    def __contains__(self, item: T) -> bool:
        """Return ``True`` if some element equals ``item``. O(n)."""
        return any(val == item for val in self)

    def _normalize_index(self, index: int, /) -> int:
        """Convert a possibly negative index into a position in ``0 .. len - 1``.

        Parameters
        ----------
        index : int
            Position as given by the caller.

        Returns
        -------
        int
            The equivalent non-negative position.

        Raises
        ------
        IndexOutOfRangeError
            If ``index`` is outside ``-len .. len - 1``.
        """
        if index < 0:
            index += self._length
        if index < 0 or index >= self._length:
            raise IndexOutOfRangeError(
                f"{type(self).__name__} index {index} out of range for length {self._length}"
            )
        return index

    def get_first(self) -> T:
        """Return the first value without removing it. O(1).

        Returns
        -------
        T
            The first element.

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        self._ensure_not_empty()
        current = cast(NodeT, self._head)
        value: T = current.value
        return value

    def get_last(self) -> T:
        """Return the last value without removing it. O(1).

        The value is read from the tail pointer, so no walk is needed.

        Returns
        -------
        T
            The last element.

        Raises
        ------
        EmptyError
            If the list is empty.
        """
        self._ensure_not_empty()
        tail = cast(NodeT, self._tail)
        value: T = tail.value
        return value

    def get_at(self, index: int, /) -> T:
        """Return the value at ``index``. O(n).

        Same as ``items[index]``.

        Parameters
        ----------
        index : int
            Position of the element, in ``-len .. len - 1``.

        Returns
        -------
        T
            The value at that position.

        Raises
        ------
        IndexOutOfRangeError
            If ``index`` is outside ``-len .. len - 1``.
        """
        return self[index]

    def index_of(self, value: T, /) -> int:
        """Return the position of the first element equal to ``value``. O(n).

        Parameters
        ----------
        value : T
            The value to look for.

        Returns
        -------
        int
            Zero-based position of the first match, or ``-1`` if there is none.
        """
        for ind, val in enumerate(self):
            if value == val:
                return ind
        return -1

    def count(self, value: T, /) -> int:
        """Return how many elements equal ``value``. O(n).

        Parameters
        ----------
        value : T
            The value to count.

        Returns
        -------
        int
            The number of matching elements, ``0`` if there are none.
        """
        count = 0
        for val in self:
            if value == val:
                count += 1
        return count

    def remove(self, value: T, /) -> bool:
        """Remove the first element equal to ``value``. O(n).

        Never raises for a missing value, and an empty list simply has nothing to
        remove. The element is located with :meth:`index_of` and unlinked with
        :meth:`remove_at`.

        Parameters
        ----------
        value : T
            The value to remove.

        Returns
        -------
        bool
            ``True`` if an element was removed, ``False`` otherwise.

        Examples
        --------
        >>> from pydsa.linear import SinglyList
        >>> items = SinglyList[int]()
        >>> for value in (1, 2, 1):
        ...     items.insert_last(value)
        >>> items.remove(1), list(items)
        (True, [2, 1])
        >>> items.remove(9)
        False
        """
        index = self.index_of(value)
        if index == -1:
            return False
        self.remove_at(index)
        return True

    def copy(self) -> Self:
        """Return a shallow copy of the list. O(n) time, O(n) space.

        The copy has the same type and its own nodes, but the stored values are
        shared, not copied.

        Returns
        -------
        Self
            A new list with the same elements in the same order.

        Examples
        --------
        >>> from pydsa.linear import SinglyList
        >>> original = SinglyList[int]()
        >>> original.insert_last(1)
        >>> clone = original.copy()
        >>> clone.insert_last(2)
        >>> list(original), list(clone)
        ([1], [1, 2])
        """
        new_list = type(self)()
        for val in self:
            new_list.insert_last(val)
        return new_list

    def clear(self) -> None:
        """Remove every element. O(1).

        The detached nodes are released to Python's garbage collector.
        """
        self._head = None
        self._tail = None
        self._length = 0

    def middle(self) -> T | tuple[T, T]:
        """Return the middle element, or the two middle elements. O(n).

        Returns
        -------
        T or tuple of (T, T)
            The middle value when the length is odd. When the length is even, the two
            middle values as a pair, in list order. Since only even lengths give a
            tuple, the result is ambiguous if the elements are tuples themselves.

        Raises
        ------
        EmptyError
            If the list is empty.

        Examples
        --------
        >>> from pydsa.linear import SinglyList
        >>> items = SinglyList[int]()
        >>> for value in (1, 2, 3):
        ...     items.insert_last(value)
        >>> items.middle()
        2
        >>> items.insert_last(4)
        >>> items.middle()
        (2, 3)
        """
        self._ensure_not_empty()
        is_even = self._length % 2 == 0
        index = self._length // 2
        if is_even:
            index -= 1
        current = self._node_at(index)
        if is_even:
            next_node = cast(NodeT, current.next)
            left: T = current.value
            right: T = next_node.value
            return left, right
        value: T = current.value
        return value

    def has_cycle(self) -> bool:
        """Return ``True`` if following ``next`` links never reaches the end. O(n).

        Uses Floyd's tortoise-and-hare algorithm with O(1) extra space. A list built
        only through its public methods cannot contain a cycle, so the result is
        ``False`` unless the internal links have been tampered with.

        Returns
        -------
        bool
            Whether the chain of nodes loops back on itself.
        """
        fast: NodeT | None = self._head
        slow: NodeT | None = self._head
        while fast is not None and fast.next is not None:
            fast = fast.next.next
            slow = slow.next if slow is not None else None
            if fast is not None and fast == slow:
                return True
        return False

    @abstractmethod
    def _node_at(self, index: int, /) -> NodeT:
        """Return the node at ``index``.

        Parameters
        ----------
        index : int
            A position already inside ``0 .. len - 1``. The caller validates it; this
            method does not.

        Returns
        -------
        NodeT
            The node at that position. Each subclass decides how to reach it.
        """

    @abstractmethod
    def insert_first(self, value: T, /) -> None:
        """Insert ``value`` at the front of the list.

        Parameters
        ----------
        value : T
            The value to insert.
        """

    @abstractmethod
    def insert_last(self, value: T, /) -> None:
        """Append ``value`` to the end of the list.

        Parameters
        ----------
        value : T
            The value to append.
        """

    @abstractmethod
    def insert_at(self, index: int, value: T, /) -> None:
        """Insert ``value`` so that it ends up at position ``index``.

        Positions ``0 .. len`` are valid and ``len`` appends. A negative index is first
        shifted by the length, so ``-1`` inserts before the last element, as
        ``list.insert`` does.

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

    @abstractmethod
    def remove_first(self) -> T:
        """Remove and return the first element.

        Returns
        -------
        T
            The removed value.

        Raises
        ------
        EmptyError
            If the list is empty.
        """

    @abstractmethod
    def remove_last(self) -> T:
        """Remove and return the last element.

        Returns
        -------
        T
            The removed value.

        Raises
        ------
        EmptyError
            If the list is empty.
        """

    @abstractmethod
    def remove_at(self, index: int, /) -> T:
        """Remove and return the element at ``index``.

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

    @abstractmethod
    def reverse(self) -> None:
        """Reverse the list in place."""
