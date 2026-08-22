"""Non-comparison sorting algorithms.

Provides counting sort, radix sort, and bucket sort — algorithms that
sort by value distribution rather than pairwise comparison.
"""

from collections.abc import Sequence


def counting_sort(arr: Sequence[int], /) -> list[int]:
    """Sort by counting frequency of each distinct value.

    Works only with non-negative integers. Counts occurrences of each value,
    builds prefix sum array, then places elements directly into sorted positions.
    Stable due to reverse-order iteration during placement.

    Time Complexity: O(n + k) where k = max(arr)
    Space Complexity: O(k)

    Parameters
    ----------
    arr : Sequence[int]
        Sequence of non-negative integers.

    Returns
    -------
    list[int]
        Sorted copy of input.

    Raises
    ------
    ValueError
        If any element is negative.

    Notes
    -----
    Stable: Yes — processes elements in reverse order to preserve order.
    Non-comparison: Uses value frequencies, not pairwise comparisons.
    Suitable only when k (range) is small relative to n.
    For negative values, shift sequence by -min(arr) before sorting.

    Examples
    --------
    >>> counting_sort([4, 2, 2, 8, 3, 3, 1])
    [1, 2, 2, 3, 3, 4, 8]

    >>> counting_sort([100, 50, 75, 25, 100])
    [25, 50, 75, 100, 100]
    """
    n = len(arr)
    if n <= 1:
        return list(arr)

    if any(num < 0 for num in arr):
        raise ValueError("counting_sort requires non-negative integers")

    max_value = max(arr)
    count = [0] * (max_value + 1)

    for num in arr:
        count[num] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    output = [0] * n
    for num in reversed(arr):
        output[count[num] - 1] = num
        count[num] -= 1

    return output


def radix_sort(arr: Sequence[int], /) -> list[int]:
    """Sort using least-significant-digit (LSD) radix sort approach.

    Processes digits from right to left (units, tens, hundreds, ...).
    Each pass uses stable counting sort on digit values (0-9), preserving
    order established by previous passes.

    Time Complexity: O(n × d) where d = number of digits in max(arr)
    Space Complexity: O(n + k) where k = 10 (digit range)

    Parameters
    ----------
    arr : Sequence[int]
        Sequence of non-negative integers.

    Returns
    -------
    list[int]
        Sorted copy of input.

    Raises
    ------
    ValueError
        If any element is negative.

    Notes
    -----
    Stable: Yes — each digit pass uses stable counting sort.
    Non-comparison: Works on digit values, not pairwise comparisons.
    Efficient for integers with moderate digit count.
    For negative values, shift sequence by -min(arr) before sorting.

    Examples
    --------
    >>> radix_sort([170, 45, 75, 90, 2, 802, 24, 2, 66])
    [2, 2, 24, 45, 66, 75, 90, 170, 802]

    >>> radix_sort([121, 432, 564, 23, 1])
    [1, 23, 121, 432, 564]
    """
    n = len(arr)
    if n <= 1:
        return list(arr)

    if any(num < 0 for num in arr):
        raise ValueError("radix_sort requires non-negative integers")

    max_value = max(arr)
    exp = 1
    output = list(arr)

    while max_value // exp > 0:
        count = [0] * 10
        for num in output:
            idx = (num // exp) % 10
            count[idx] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        copied = [0] * n
        for num in reversed(output):
            idx = (num // exp) % 10
            copied[count[idx] - 1] = num
            count[idx] -= 1

        output = copied
        exp *= 10

    return output


def bucket_sort(arr: Sequence[float], /) -> list[float]:
    """Sort by distributing elements into buckets, then sorting each bucket.

    Divides value range into n buckets, distributes elements proportionally,
    then sorts each bucket using insertion sort. Average O(n) on uniformly
    distributed data.

    Time Complexity: O(n) average, O(n²) worst case
    Space Complexity: O(n)

    Parameters
    ----------
    arr : Sequence[float]
        Sequence of numeric values (floats or integers).

    Returns
    -------
    list[float]
        Sorted copy of input.

    Notes
    -----
    Stable: Yes — insertion sort within each bucket is stable.
    Non-comparison: Distribution-based, not pairwise comparisons.
    Bucket assignment: idx = (value - min) / (max - min) * (n - 1)
    Best for uniformly distributed data across known range.
    Worst-case O(n²) when all elements fall into a single bucket.

    Examples
    --------
    >>> bucket_sort([0.4, 0.1, 0.7, 0.3, 0.9])
    [0.1, 0.3, 0.4, 0.7, 0.9]

    >>> bucket_sort([5, 2, 8, 1, 9, 3])
    [1, 2, 3, 5, 8, 9]
    """
    n = len(arr)
    if n <= 1:
        return list(arr)

    min_val = min(arr)
    max_val = max(arr)

    if min_val == max_val:
        return list(arr)

    counts = [0] * n
    for num in arr:
        idx = int(((num - min_val) / (max_val - min_val)) * (n - 1))
        counts[idx] += 1

    starts = [0] * n
    for i in range(1, n):
        starts[i] = starts[i - 1] + counts[i - 1]

    output = [0.0] * n
    temp_counts = [0] * n
    for num in arr:
        idx = int(((num - min_val) / (max_val - min_val)) * (n - 1))
        pos = starts[idx] + temp_counts[idx]
        output[pos] = num
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
