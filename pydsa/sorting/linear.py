import numpy as np
from numba import njit


@njit  # type: ignore
def counting_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using counting sort. O(n + k) time, O(k) space.

    Counts the frequency of each distinct integer value, then uses
    a prefix sum to place each element directly into its sorted
    position. Works only with non-negative integer arrays.

    Parameters
    ----------
    arr : np.ndarray
        Input array of non-negative integers.

    Returns
    -------
    np.ndarray
        Sorted copy of the input array.

    Notes
    -----
    - **Stable**: Yes — processes elements in reverse order.
    - **Non-comparison**: Uses value frequencies, not pairwise comparisons.
    - **Space**: O(k) where k = max(arr). Suitable only when k is
      reasonably small relative to n.
    - For arrays with negative values, shift by ``-min(arr)`` before sorting.
    """
    n = arr.shape[0]
    if n <= 1:
        return arr.copy()
    max_value = np.max(arr)
    count = np.full(max_value + 1, 0, dtype=np.int32)
    for i in range(n):
        count[arr[i]] += 1
    for i in range(1, count.shape[0]):
        count[i] += count[i - 1]
    output = np.zeros_like(arr)
    for i in range(n - 1, -1, -1):
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
    return output


@njit  # type: ignore
def radix_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using LSD radix sort. O(n × d) time, O(n + k) space.

    Sorts integers digit by digit starting from the least significant
    digit (LSD). Each pass uses a stable counting sort over the range
    [0, 9], preserving the order from previous passes.

    Parameters
    ----------
    arr : np.ndarray
        Input array of non-negative integers.

    Returns
    -------
    np.ndarray
        Sorted copy of the input array.

    Notes
    -----
    - **Stable**: Yes — each digit pass uses a stable counting sort.
    - **Non-comparison**: Works on digits, not pairwise comparisons.
    - **Time**: O(n × d) where d = number of digits in max(arr).
    - Handles duplicates and large values efficiently as long as
      the number of digits is moderate.
    - For negative integers, shift by ``-min(arr)`` before sorting.
    """
    n = arr.shape[0]
    if n <= 1:
        return arr.copy()
    max_value = np.max(arr)
    exp = 1
    output = arr.copy()
    while max_value // exp > 0:
        count = np.full(10, 0, dtype=np.int32)
        for i in range(n):
            idx = (output[i] // exp) % 10
            count[idx] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        copied = np.zeros_like(output)
        for i in range(n - 1, -1, -1):
            idx = (output[i] // exp) % 10
            copied[count[idx] - 1] = output[i]
            count[idx] -= 1
        for i in range(n):
            output[i] = copied[i]
        exp *= 10
    return output


@njit  # type: ignore
def bucket_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using bucket sort. O(n + k) average time, O(n) space.

    Distributes elements into n buckets based on their value range,
    then sorts each bucket using insertion sort. Best suited for
    uniformly distributed data.

    Parameters
    ----------
    arr : np.ndarray
        Input array (floats or integers).

    Returns
    -------
    np.ndarray
        Sorted copy of the input array.

    Notes
    -----
    - **Stable**: Yes — uses stable insertion sort within each bucket.
    - **Non-comparison**: Distribution-based, not pairwise comparisons.
    - **Worst case O(n²)**: Occurs when all elements fall into a single bucket.
    - Bucket index formula: ``(value - min) / (max - min) * (n - 1)``.
    - For data that is already uniform, runs in linear time.
    """
    n = arr.shape[0]
    if n <= 1:
        return arr.copy()
    min_val = np.min(arr)
    max_val = np.max(arr)
    if min_val == max_val:
        return arr.copy()

    counts = np.zeros(n, dtype=np.int32)
    for i in range(n):
        idx = int(((arr[i] - min_val) / (max_val - min_val)) * (n - 1))
        counts[idx] += 1

    starts = np.zeros(n, dtype=np.int32)
    for i in range(1, n):
        starts[i] = starts[i - 1] + counts[i - 1]

    output = np.zeros_like(arr)
    temp_counts = np.zeros(n, dtype=np.int32)
    for i in range(n):
        idx = int(((arr[i] - min_val) / (max_val - min_val)) * (n - 1))
        pos = starts[idx] + temp_counts[idx]
        output[pos] = arr[i]
        temp_counts[idx] += 1

    for i in range(n):
        if counts[i] > 1:
            start = starts[i]
            end = start + counts[i]
            for p in range(start + 1, end):
                key = output[p]
                q = p - 1
                while q >= start and output[q] > key:
                    output[q + 1] = output[q]
                    q -= 1
                output[q + 1] = key

    return output
