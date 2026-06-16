import numpy as np
from numba import njit


@njit # type: ignore
def linear_search(arr: np.ndarray, target: int, /) -> int:
    """
    Linear search — O(n) time, O(1) space.

    Sequentially checks each element until the target is found.
    Works on unsorted arrays.

    Parameters
    ----------
    arr : np.ndarray
        Input array.
    target : Any
        Value to search for.

    Returns
    -------
    int
        Index of the first occurrence, or -1 if not found.
    """
    for i in range(arr.shape[0]):
        if arr[i] == target:
            return i
    return -1


@njit # type: ignore
def binary_search(arr: np.ndarray, target: int, /) -> int:
    """
    Binary search — O(log n) time, O(1) space.

    Requires a sorted array. Repeatedly halves the search interval
    by comparing the target with the middle element.

    Parameters
    ----------
    arr : np.ndarray
        Sorted input array.
    target : Any
        Value to search for.

    Returns
    -------
    int
        Index of the target, or -1 if not found.
    """
    left = 0
    right = arr.shape[0] - 1
    while left <= right:
        midd_idx = int((left + right) // 2)
        if target == arr[midd_idx]:
            return midd_idx
        elif target < arr[midd_idx]:
            right = midd_idx - 1
        else:
            left = midd_idx + 1
    return -1


@njit # type: ignore
def jump_search(arr: np.ndarray, target: int, /) -> int:
    """
    Jump search — O(√n) time, O(1) space.

    Requires a sorted array. Jumps ahead by a fixed step of √n,
    then performs a linear search in the identified block.

    Parameters
    ----------
    arr : np.ndarray
        Sorted input array.
    target : Any
        Value to search for.

    Returns
    -------
    int
        Index of the target, or -1 if not found.
    """
    n = arr.shape[0]
    step = int(np.sqrt(n))
    high = step
    while high < n and arr[high] < target:
        high += step
    low = max(0, high - step)
    high = min(high + 1, n)
    for i in range(low, high):
        if target == arr[i]:
            return i
    return -1


@njit # type: ignore
def exponential_search(arr: np.ndarray, target: int, /) -> int:
    """
    Exponential search — O(log n) time, O(1) space.

    Requires a sorted array. Finds a range by repeatedly doubling
    the bound (1, 2, 4, 8, ...), then performs binary search
    within that range. Ideal for unbounded or large arrays where
    the target is near the beginning.

    Parameters
    ----------
    arr : np.ndarray
        Sorted input array.
    target : Any
        Value to search for.

    Returns
    -------
    int
        Index of the target, or -1 if not found.
    """
    n = arr.shape[0]
    high = 1
    while high < n and arr[high] < target:
        high *= 2
    left = high // 2
    right = min(high, n - 1)
    while left <= right:
        midd_idx = int((left + right) // 2)
        if target == arr[midd_idx]:
            return midd_idx
        elif target < arr[midd_idx]:
            right = midd_idx - 1
        else:
            left = midd_idx + 1
    return -1
