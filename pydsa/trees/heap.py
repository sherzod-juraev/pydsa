"""Binary heap implementations.

Provides :class:`MinHeap` and :class:`MaxHeap`, binary heaps backed by a dynamic
array, built on the shared :class:`HeapBase`. Both use Floyd's linear-time heapify
algorithm.
"""

from abc import abstractmethod

from ..core import BaseStructure, Comparable


class HeapBase[T: Comparable](BaseStructure):
    """Abstract foundation of the binary heaps.

    A heap is a complete binary tree stored in an array, in which every parent
    precedes its children. The element that precedes all the others is always at
    the root (index 0), accessible in O(1) time. What "precedes" means is decided by
    the single abstract method ``_precedes``: the minimum comes first in a min-heap
    and the maximum in a max-heap. Everything else is written once, here.

    Time Complexity Summary

    .. csv-table:: Array Index Relations (0-based)
       :header: "Relation", "Formula"
       :widths: 20, 25

       "parent", "(i - 1) // 2"
       "left child", "2 * i + 1"
       "right child", "2 * i + 2"

    Time Complexity Summary

    .. csv-table:: Heap Base Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 15, 10

       "insert", "O(log n)", "O(1)"
       "peek", "O(1)", "O(1)"
       "heapify", "O(n)", "O(n)"
       "extract_all", "O(n log n)", "O(n)"
       "__contains__", "O(n)", "O(1)"
       "__len__", "O(1)", "O(1)"
       "clear", "O(1)", "O(1)"

    Notes
    -----
    - Not meant to be used directly and not exported from :mod:`pydsa.trees`.
    - Uses Floyd's linear-time algorithm for ``heapify``.
    - ``extract_all`` empties the heap and returns the elements in priority order,
      which is a heap sort.
    - Subclasses implement ``_precedes`` and add one public method that removes the
      root under a name that states the order, such as ``extract_min``.
    """

    def __init__(self) -> None:
        """Initialize an empty heap."""
        self._data: list[T] = []

    def __len__(self) -> int:
        """Return the number of elements. O(1)."""
        return len(self._data)

    def __contains__(self, item: T) -> bool:
        """Return True if the value exists in the heap. O(n)."""
        return item in self._data

    def clear(self) -> None:
        """Remove all elements from the heap. O(1)."""
        self._data.clear()

    def peek(self) -> T:
        """Return the root value without removing it. O(1).

        The root is the element that precedes all the others: the minimum in a
        min-heap and the maximum in a max-heap.

        Raises
        ------
        EmptyError
            If the heap is empty.
        """
        self._ensure_not_empty()
        return self._data[0]

    def insert(self, value: T, /) -> None:
        """Insert a value into the heap. O(log n).

        The value is appended to the end of the array and bubbled up until the heap
        invariant is restored.

        Parameters
        ----------
        value : T
            The value to insert.
        """
        self._data.append(value)
        self._shift_up(len(self._data) - 1)

    def extract_all(self) -> list[T]:
        """Remove all elements and return them in priority order. O(n log n).

        This empties the heap. Equivalent to performing heap sort: ascending order
        for a min-heap and descending order for a max-heap.

        Returns
        -------
        list
            The values in priority order, root first.
        """
        return [self._extract_root() for _ in range(len(self))]

    def heapify(self, arr: list[T], /) -> None:
        """Build a heap from an existing list in O(n) time.

        Uses Floyd's algorithm: starting from the last non-leaf node and bubbling
        down each parent up to the root. Any elements the heap held before are
        discarded.

        Parameters
        ----------
        arr : list
            The list from which to build the heap. A copy is made, so the list is
            never modified.
        """
        self._data = arr.copy()
        for index in range(len(self._data) // 2 - 1, -1, -1):
            self._shift_down(index)

    @abstractmethod
    def _precedes(self, first: T, second: T, /) -> bool:
        """Return True if ``first`` must be closer to the root than ``second``.

        The relation must be strict: two equal values never precede each other.

        Parameters
        ----------
        first : T
            The value being placed.
        second : T
            The value it is compared with.
        """

    def _extract_root(self) -> T:
        """Remove and return the root value. O(log n).

        The root is swapped with the last element, removed, and the new root is
        bubbled down to restore the invariant.

        Raises
        ------
        EmptyError
            If the heap is empty.
        """
        self._ensure_not_empty()
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._shift_down(0)
        return root

    def _shift_up(self, child: int, /) -> None:
        """Bubble the element at the given index up to its correct position."""
        while child > 0:
            parent = (child - 1) // 2
            if not self._precedes(self._data[child], self._data[parent]):
                break
            self._swap(parent, child)
            child = parent

    def _shift_down(self, parent: int, /) -> None:
        """Bubble the element at the given index down to its correct position."""
        size = len(self._data)
        while True:
            left = parent * 2 + 1
            right = parent * 2 + 2
            first = parent
            if left < size and self._precedes(self._data[left], self._data[first]):
                first = left
            if right < size and self._precedes(self._data[right], self._data[first]):
                first = right
            if first == parent:
                break
            self._swap(parent, first)
            parent = first

    def _swap(self, i: int, j: int, /) -> None:
        """Swap two elements by index."""
        self._data[i], self._data[j] = self._data[j], self._data[i]


class MinHeap[T: Comparable](HeapBase[T]):
    """A binary min-heap implemented with a dynamic array.

    The heap is a complete binary tree where every parent is less than or equal to
    its children. The minimum element is always at the root (index 0), accessible in
    O(1) time.

    Time Complexity Summary

    .. csv-table:: Min-Heap Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 15, 10

       "insert", "O(log n)", "O(1)"
       "extract_min", "O(log n)", "O(1)"
       "peek", "O(1)", "O(1)"
       "heapify", "O(n)", "O(n)"
       "extract_all", "O(n log n)", "O(n)"
       "__contains__", "O(n)", "O(1)"

    Notes
    -----
    - Uses Floyd's linear-time algorithm for ``heapify``.
    - ``extract_all`` empties the heap and returns the elements in sorted ascending
      order (heap sort).
    - For a max-heap, see ``MaxHeap``.

    Examples
    --------
    >>> heap = MinHeap[int]()
    >>> for value in [9, 3, 7]:
    ...     heap.insert(value)
    >>> heap.peek()
    3
    >>> heap.extract_all()
    [3, 7, 9]
    """

    def _precedes(self, first: T, second: T, /) -> bool:
        """Return True if ``first`` is smaller than ``second``."""
        return first < second

    def extract_min(self) -> T:
        """Remove and return the minimum value. O(log n).

        Raises
        ------
        EmptyError
            If the heap is empty.

        Examples
        --------
        >>> heap = MinHeap[int]()
        >>> for value in [9, 3, 1]:
        ...     heap.insert(value)
        >>> heap.extract_min()
        1
        >>> heap.extract_min()
        3
        """
        return self._extract_root()


class MaxHeap[T: Comparable](HeapBase[T]):
    """A binary max-heap implemented with a dynamic array.

    The heap is a complete binary tree where every parent is greater than or equal
    to its children. The maximum element is always at the root (index 0), accessible
    in O(1) time.

    Time Complexity Summary

    .. csv-table:: Max-Heap Operations Complexity
       :header: "Operation", "Time", "Space"
       :widths: 20, 15, 10

       "insert", "O(log n)", "O(1)"
       "extract_max", "O(log n)", "O(1)"
       "peek", "O(1)", "O(1)"
       "heapify", "O(n)", "O(n)"
       "extract_all", "O(n log n)", "O(n)"
       "__contains__", "O(n)", "O(1)"

    Notes
    -----
    - Uses Floyd's linear-time algorithm for ``heapify``.
    - ``extract_all`` empties the heap and returns the elements in sorted descending
      order (heap sort).
    - For a min-heap, see ``MinHeap``.

    Examples
    --------
    >>> heap = MaxHeap[int]()
    >>> for value in [3, 9, 7]:
    ...     heap.insert(value)
    >>> heap.peek()
    9
    >>> heap.extract_all()
    [9, 7, 3]
    """

    def _precedes(self, first: T, second: T, /) -> bool:
        """Return True if ``first`` is greater than ``second``."""
        return second < first

    def extract_max(self) -> T:
        """Remove and return the maximum value. O(log n).

        Raises
        ------
        EmptyError
            If the heap is empty.

        Examples
        --------
        >>> heap = MaxHeap[int]()
        >>> for value in [3, 9, 1]:
        ...     heap.insert(value)
        >>> heap.extract_max()
        9
        >>> heap.extract_max()
        3
        """
        return self._extract_root()
