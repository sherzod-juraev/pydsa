import numpy as np


def merge_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using merge sort. O(n log n) time, O(n) space.

    Recursively divides the array into two halves, sorts each half,
    and merges the sorted halves back together. The merge step
    preserves the relative order of equal elements, making this
    a stable sorting algorithm.

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
    - **Stable**: Yes — equal elements preserve their original order.
    - **Divide-and-conquer**: Splits array in half at each recursion level.
    - **Space**: Requires O(n) auxiliary array for merging.
    - Performs consistently in O(n log n) regardless of input distribution,
      unlike Quick Sort which degrades to O(n²) on sorted/reverse input.
    """
    n = arr.shape[0]
    if n <= 1:
        return arr.copy()

    arr_left = arr[: (n // 2)].copy()
    arr_right = arr[(n // 2) :].copy()

    arr_left = merge_sort(arr_left)
    arr_right = merge_sort(arr_right)

    a = 0
    b = 0
    c = 0
    merged = np.zeros(shape=arr_left.shape[0] + arr_right.shape[0], dtype=arr.dtype)
    while a < arr_left.shape[0] and b < arr_right.shape[0]:
        if arr_left[a] < arr_right[b]:
            merged[c] = arr_left[a]
            a += 1
        else:
            merged[c] = arr_right[b]
            b += 1
        c += 1
    while a < arr_left.shape[0]:
        merged[c] = arr_left[a]
        a += 1
        c += 1
    while b < arr_right.shape[0]:
        merged[c] = arr_right[b]
        b += 1
        c += 1
    return merged


def quick_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using quick sort. O(n log n) average, O(n²) worst time. O(log n) space.

    Selects a pivot element (the last element), partitions the array
    so that elements smaller than the pivot are on the left and larger
    on the right, then recursively sorts both partitions.

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
    - **Stable**: No — equal elements may be reordered during partitioning.
    - **Divide-and-conquer**: Partitions around a pivot, then recurses.
    - **In-place**: Operates on a copy; original is unchanged. O(log n) stack space.
    - **Pivot selection**: Uses the last element (Lomuto partition scheme).
      This degrades to O(n²) on already-sorted or reverse-sorted input.
      Random or median-of-three pivot selection mitigates this in practice.
    - Performs well on average and is often faster than merge sort due to
      cache locality and low constant factors.
    """
    def _quick_sort(arr: np.ndarray, low: int, high: int, /) -> None:
        if low < high:
            pi = _partition(arr, low, high)
            _quick_sort(arr, low, pi - 1)
            _quick_sort(arr, pi + 1, high)

    def _partition(arr: np.ndarray, low: int, high: int, /) -> int:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[high], arr[i + 1] = arr[i + 1], arr[high]
        return i + 1

    copied = arr.copy()
    _quick_sort(copied, 0, arr.shape[0] - 1)
    return copied
