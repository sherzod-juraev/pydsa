import numpy as np
from numba import njit


@njit
def bubble_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using bubble sort. O(n²) time, O(n) space.

    Repeatedly steps through the array, compares adjacent elements,
    and swaps them if they are in the wrong order. The largest
    element "bubbles" to the end in each pass. Early termination
    occurs if no swaps are made in a pass, giving O(n) best case
    for already-sorted input.

    Parameters
    ----------
    arr : np.ndarray
        Input array.

    Returns
    -------
    np.ndarray
        Sorted copy of the input array.

    Notes
    -----
    - **Stable**: Yes.
    - **In-place**: Operates on a copy; original is unchanged.
    - Compiled with ``@njit`` (Numba) for C-level loop performance.
    """
    copied = arr.copy()
    n = copied.shape[0]
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if copied[j + 1] < copied[j]:
                copied[j], copied[j + 1] = copied[j + 1], copied[j]
                swapped = True
        if not swapped:
            break
    return copied


@njit
def selection_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using selection sort. O(n²) time, O(n) space.

    Divides the array into a sorted and unsorted region. In each
    iteration, the smallest element from the unsorted region is
    selected and placed at the end of the sorted region.

    Parameters
    ----------
    arr : np.ndarray
        Input array.

    Returns
    -------
    np.ndarray
        Sorted copy of the input array.

    Notes
    -----
    - **Stable**: No (swapping may change order of equal elements).
    - **In-place**: Operates on a copy; original is unchanged.
    - Does O(n²) comparisons even on sorted input — not adaptive.
    - Compiled with ``@njit`` (Numba) for C-level loop performance.
    """
    copied = arr.copy()
    n = copied.shape[0]
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if copied[j] < copied[min_idx]:
                min_idx = j
        if i != min_idx:
            copied[i], copied[min_idx] = copied[min_idx], copied[i]
    return copied


@njit
def insertion_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using insertion sort. O(n²) time, O(n) space.

    Builds the sorted array one element at a time by taking each
    element and inserting it into its correct position among the
    previously sorted elements. Efficient for small or partially
    sorted datasets — O(n) best case when the array is already sorted.

    Parameters
    ----------
    arr : np.ndarray
        Input array.

    Returns
    -------
    np.ndarray
        Sorted copy of the input array.

    Notes
    -----
    - **Stable**: Yes.
    - **Adaptive**: O(n) best case for already-sorted input.
    - **In-place**: Operates on a copy; original is unchanged.
    - Compiled with ``@njit`` (Numba) for C-level loop performance.
    """
    copied = arr.copy()
    n = copied.shape[0]
    for i in range(n - 1):
        j = i + 1
        value = copied[j]
        while j > 0 and value < copied[j - 1]:
            copied[j] = copied[j - 1]
            j -= 1
        copied[j] = value
    return copied