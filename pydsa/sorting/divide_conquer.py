"""Divide-and-conquer sorting algorithms.

Provides iterative (non-recursive) merge sort and quick sort.
"""

from collections.abc import Sequence

from .._types import Comparable
from ..linear import Stack


def merge_sort[T: Comparable](arr: Sequence[T], /) -> list[T]:
    """Sort using iterative bottom-up merge approach.

    Divides array into incrementally larger subarrays (size 1, 2, 4, 8, ...)
    and merges pairs repeatedly. No recursion — uses explicit iteration.

    Time Complexity: O(n log n) in all cases
    Space Complexity: O(n)

    Parameters
    ----------
    arr : Sequence[T]
        Input sequence.

    Returns
    -------
    list[T]
        Sorted copy of input.

    Notes
    -----
    Stable: Yes — merging preserves relative order of equal elements.
    Bottom-up iterative approach eliminates recursion depth concerns.
    Requires O(n) auxiliary space for temporary arrays during merge.
    Predictable performance regardless of input distribution.

    Examples
    --------
    >>> merge_sort([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]

    >>> merge_sort(["dog", "cat", "elephant", "ant"])
    ['ant', 'cat', 'dog', 'elephant']
    """
    n = len(arr)
    if n <= 1:
        return list(arr)

    source = list(arr)
    target: list[T] = [source[0]] * n

    size = 1

    while size < n:
        for left_start in range(0, n, 2 * size):
            mid = min(left_start + size, n)
            right_end = min(left_start + 2 * size, n)

            _merge_subarrays(source, target, left_start, mid, right_end)

        source, target = target, source
        size *= 2

    return source


def _merge_subarrays[T: Comparable](
    source: list[T],
    target: list[T],
    left: int,
    mid: int,
    right: int,
    /,
) -> None:
    """Merge two sorted subarrays into target using two-pointer technique.

    Merges source[left:mid] and source[mid:right] into target[left:right].
    Maintains stable order when equal elements are encountered.

    Parameters
    ----------
    source : list[T]
        Source array containing two sorted subarrays.
    target : list[T]
        Target array to write merged result.
    left : int
        Start index of first subarray.
    mid : int
        Boundary (end of first, start of second subarray).
    right : int
        End index of second subarray.
    """
    if mid >= right:
        for i in range(left, right):
            target[i] = source[i]
        return

    i = left
    j = mid
    k = left

    while i < mid and j < right:
        if source[i] <= source[j]:
            target[k] = source[i]
            i += 1
        else:
            target[k] = source[j]
            j += 1
        k += 1

    while i < mid:
        target[k] = source[i]
        i += 1
        k += 1

    while j < right:
        target[k] = source[j]
        j += 1
        k += 1


def quick_sort[T: Comparable](arr: Sequence[T], /) -> list[T]:
    """Sort using iterative quick sort with custom Stack.

    Uses explicit Stack to simulate recursion, avoiding stack overflow
    on large or pathological inputs. Pushes smaller subarray first to
    maintain O(log n) stack depth. Uses Lomuto partition scheme.

    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) — stack depth

    Parameters
    ----------
    arr : Sequence[T]
        Input sequence.

    Returns
    -------
    list[T]
        Sorted copy of input.

    Notes
    -----
    Unstable: Equal elements may be reordered during partitioning.
    Uses Lomuto partition (simpler, slightly slower than Hoare scheme).
    Iterative approach prevents recursion depth issues on large arrays.
    Worst-case O(n²) occurs on already-sorted or reverse-sorted input.

    Examples
    --------
    >>> quick_sort([38, 27, 43, 3, 9, 82, 10])
    [3, 9, 10, 27, 38, 43, 82]

    >>> quick_sort(["dog", "cat", "elephant", "ant"])
    ['ant', 'cat', 'dog', 'elephant']
    """
    n = len(arr)

    if n <= 1:
        return list(arr)

    result = list(arr)
    stack: Stack[tuple[int, int]] = Stack()
    stack.push((0, n - 1))

    while not stack.is_empty():
        low, high = stack.pop()
        if low < high:
            pivot_idx = _lomuto_partition(result, low, high)
            left_size = pivot_idx - low
            right_size = high - pivot_idx

            if left_size < right_size:
                if pivot_idx + 1 < high:
                    stack.push((pivot_idx + 1, high))
                if low < pivot_idx - 1:
                    stack.push((low, pivot_idx - 1))
            else:
                if low < pivot_idx - 1:
                    stack.push((low, pivot_idx - 1))
                if pivot_idx + 1 < high:
                    stack.push((pivot_idx + 1, high))

    return result


def _lomuto_partition[T: Comparable](arr: list[T], low: int, high: int, /) -> int:
    """Partition array using Lomuto scheme with last element as pivot.

    Rearranges array so all elements <= pivot come before it, all > pivot
    come after. Returns the final position of the pivot element.

    Parameters
    ----------
    arr : list[T]
        Array to partition (modified in-place).
    low : int
        Start index of partition range.
    high : int
        End index and pivot position.

    Returns
    -------
    int
        Final position of the pivot element.
    """
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[high], arr[i + 1] = arr[i + 1], arr[high]

    return i + 1
