"""Heap sort.

Provides heap sort built on top of :class:`~pydsa.trees.MinHeap`.
"""

from collections.abc import Sequence

from .._types import Comparable
from ..trees import MinHeap


def heap_sort[T: Comparable](arr: Sequence[T], /) -> list[T]:
    """Sort using min-heap with Floyd's O(n) heapify algorithm.

    Builds a min-heap from input in O(n) time using bottom-up heapify,
    then extracts minimum repeatedly to produce sorted output.

    Time Complexity: O(n log n)
    Space Complexity: O(n)

    Parameters
    ----------
    arr : Sequence[T]
        Input sequence of comparable elements.

    Returns
    -------
    list[T]
        Sorted copy of input in ascending order.

    Notes
    -----
    Unstable: Heap operations do not preserve relative order of equal elements.
    Uses custom MinHeap with O(n) heapify and O(n log n) extraction.
    Consistent O(n log n) performance regardless of input distribution.
    No recursion or external stack needed.

    Examples
    --------
    >>> heap_sort([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]

    >>> heap_sort(["zebra", "apple", "mango", "banana"])
    ['apple', 'banana', 'mango', 'zebra']
    """
    min_heap: MinHeap[T] = MinHeap()
    min_heap.heapify(list(arr))
    return min_heap.extract_all()
