"""Elementary sorting algorithms.

Provides bubble sort, selection sort, and insertion sort.
"""

from collections.abc import Sequence

from .._types import Comparable


def bubble_sort[T: Comparable](arr: Sequence[T], /) -> list[T]:
    """Sort by repeatedly swapping adjacent out-of-order elements.

    Largest element "bubbles" to the end each pass. Adaptive — stops early
    if no swaps occur, giving O(n) best case on already-sorted input.

    Time Complexity: O(n²) average and worst case, O(n) best case
    Space Complexity: O(n) — returns a new list, does not mutate input

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
    Stable: Yes — preserves relative order of equal elements.
    Adaptive: O(n) on already-sorted input.

    Examples
    --------
    >>> bubble_sort([5, 2, 8, 1, 9])
    [1, 2, 5, 8, 9]

    >>> bubble_sort(["zebra", "apple", "mango"])
    ['apple', 'mango', 'zebra']
    """
    copied = list(arr)
    n = len(copied)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if copied[j + 1] < copied[j]:
                copied[j], copied[j + 1] = copied[j + 1], copied[j]
                swapped = True
        if not swapped:
            break
    return copied


def selection_sort[T: Comparable](arr: Sequence[T], /) -> list[T]:
    """Sort by selecting the minimum from unsorted region each iteration.

    Divides array into sorted (left) and unsorted (right) regions.
    Each pass finds the smallest element in unsorted region and swaps to sorted.

    Time Complexity: O(n²) in all cases (best, average, worst)
    Space Complexity: O(n) — returns a new list, does not mutate input

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
    Unstable: Swap operations may reorder equal elements.
    Non-adaptive: Always O(n²) even on sorted input (no early termination).

    Examples
    --------
    >>> selection_sort([5, 2, 8, 1, 9])
    [1, 2, 5, 8, 9]

    >>> selection_sort(["zebra", "apple", "mango"])
    ['apple', 'mango', 'zebra']
    """
    copied = list(arr)
    n = len(copied)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if copied[j] < copied[min_idx]:
                min_idx = j
        if i != min_idx:
            copied[i], copied[min_idx] = copied[min_idx], copied[i]
    return copied


def insertion_sort[T: Comparable](arr: Sequence[T], /) -> list[T]:
    """Sort by inserting each element into its correct position.

    Builds sorted array one element at a time. Each element is inserted
    into the correct position among previously sorted elements. Efficient
    for small or partially sorted datasets — O(n) best case.

    Time Complexity: O(n²) average and worst case, O(n) best case
    Space Complexity: O(n) — returns a new list, does not mutate input

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
    Stable: Yes — preserves relative order of equal elements.
    Adaptive: O(n) on already-sorted input. Minimal shifts needed.
    Preferred for small arrays (< 50 elements) due to low overhead.

    Examples
    --------
    >>> insertion_sort([5, 2, 8, 1, 9])
    [1, 2, 5, 8, 9]

    >>> sorted_arr = [1, 2, 3, 4, 5]
    >>> insertion_sort(sorted_arr)  # O(n) best case
    [1, 2, 3, 4, 5]
    """
    copied = list(arr)
    n = len(copied)
    for i in range(n - 1):
        j = i + 1
        value = copied[j]
        while j > 0 and value < copied[j - 1]:
            copied[j] = copied[j - 1]
            j -= 1
        copied[j] = value
    return copied
