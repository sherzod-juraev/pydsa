"""Searching algorithms.

Provides classic search algorithms: linear, binary, jump, and
exponential search.
"""

import math
from collections.abc import Sequence

from .._types import Comparable


def linear_search[T: Comparable](arr: Sequence[T], target: T, /) -> int:
    """Search for target by checking each element sequentially.

    Time Complexity: O(n)
    Space Complexity: O(1)

    Works on unsorted arrays. No preprocessing required.

    Parameters
    ----------
    arr : Sequence[T]
        Input sequence (sorted or unsorted).
    target : T
        Value to search for.

    Returns
    -------
    int
        Index of first occurrence (0-based), or -1 if not found.

    Examples
    --------
    >>> linear_search([15, 3, 9, 1, 7], 9)
    2
    >>> linear_search([15, 3, 9, 1, 7], 100)
    -1
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


def binary_search[T: Comparable](arr: Sequence[T], target: T, /) -> int:
    """Search sorted array by repeatedly halving the search interval.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Requires: Input sequence must be sorted in ascending order.

    Parameters
    ----------
    arr : Sequence[T]
        Sorted input sequence (ascending order).
    target : T
        Value to search for.

    Returns
    -------
    int
        Index of target (0-based), or -1 if not found.

    Examples
    --------
    >>> binary_search([1, 3, 7, 9, 15], 9)
    3
    >>> binary_search([1, 3, 7, 9, 15], 5)
    -1

    Notes
    -----
    Returns incorrect results without raising exception if input is unsorted.
    Always verify input is sorted in ascending order.
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid_idx = (left + right) // 2
        if target == arr[mid_idx]:
            return mid_idx
        elif target < arr[mid_idx]:
            right = mid_idx - 1
        else:
            left = mid_idx + 1
    return -1


def jump_search[T: Comparable](arr: Sequence[T], target: T, /) -> int:
    """Search sorted array by jumping in fixed intervals, then linear search.

    Time Complexity: O(√n)
    Space Complexity: O(1)

    Requires: Input sequence must be sorted in ascending order.

    Parameters
    ----------
    arr : Sequence[T]
        Sorted input sequence (ascending order).
    target : T
        Value to search for.

    Returns
    -------
    int
        Index of target (0-based), or -1 if not found.

    Examples
    --------
    >>> jump_search([1, 3, 7, 9, 15, 20, 25, 30], 9)
    3
    >>> jump_search([1, 3, 7, 9, 15, 20, 25, 30], 20)
    5
    >>> jump_search([1, 3, 7, 9, 15, 20, 25, 30], 5)
    -1
    """
    n = len(arr)
    step = int(math.sqrt(n))
    high = step
    while high < n and arr[high] < target:
        high += step
    low = max(0, high - step)
    high = min(high + 1, n)
    for i in range(low, high):
        if target == arr[i]:
            return i
    return -1


def exponential_search[T: Comparable](arr: Sequence[T], target: T, /) -> int:
    """Search sorted array by finding range (1, 2, 4, ...), then binary search.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Requires: Input sequence must be sorted in ascending order.

    Optimal for unbounded arrays or when target is likely near the start.

    Parameters
    ----------
    arr : Sequence[T]
        Sorted input sequence (ascending order).
    target : T
        Value to search for.

    Returns
    -------
    int
        Index of target (0-based), or -1 if not found.

    Examples
    --------
    >>> exponential_search([1, 3, 5, 7, 9, 15, 20, 30, 50], 15)
    5
    >>> exponential_search([1, 3, 5, 7, 9, 15, 20, 30, 50], 50)
    8
    >>> exponential_search([1, 3, 5, 7, 9, 15, 20, 30, 50], 100)
    -1
    """
    n = len(arr)
    high = 1
    while high < n and arr[high] < target:
        high *= 2
    left = high // 2
    right = min(high, n - 1)
    while left <= right:
        mid_idx = (left + right) // 2
        if target == arr[mid_idx]:
            return mid_idx
        elif target < arr[mid_idx]:
            right = mid_idx - 1
        else:
            left = mid_idx + 1
    return -1
