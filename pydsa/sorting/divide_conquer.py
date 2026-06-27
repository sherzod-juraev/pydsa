import numpy as np

from ..linear import Stack


def merge_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using iterative bottom-up merge sort.

    No recursion, no stack - uses iterative merging of increasingly
    larger subarrays. O(n log n) time, O(n) space.

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
    - Stable: Yes - equal elements preserve their relative order
    - Bottom-up approach: starts with size=1, doubles each iteration
    - No recursion overhead, no stack allocation
    - Predictable O(n log n) performance regardless of input

    Examples
    --------
    >>> arr = np.array([38, 27, 43, 3, 9, 82, 10])
    >>> merge_sort(arr)
    array([ 3,  9, 10, 27, 38, 43, 82])
    """
    n = arr.shape[0]
    if n <= 1:
        return arr.copy()
    source = arr.copy()
    target = np.zeros_like(arr)

    size = 1

    while size < n:
        for left_start in range(0, n, 2 * size):
            mid = min(left_start + size, n)
            right_end = min(left_start + 2 * size, n)

            _merge_subarrays(source, target, left_start, mid, right_end)

        source, target = target, source
        size *= 2

    return source


def _merge_subarrays(
    source: np.ndarray,
    target: np.ndarray,
    left: int,
    mid: int,
    right: int,
    /,
) -> None:
    """
    Merge two sorted subarrays from source into target.

    Merges source[left:mid] and source[mid:right] into target[left:right].
    All indices are handled safely for partial merges at array boundaries.

    Parameters
    ----------
    source : np.ndarray
        Source array with sorted subarrays.
    target : np.ndarray
        Target array to write merged result.
    left : int
        Start index of first subarray.
    mid : int
        End of first subarray, start of second.
    right : int
        End of second subarray.
    """
    if mid >= right:
        target[left:right] = source[left:right]
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


def quick_sort(arr: np.ndarray, /) -> np.ndarray:
    """
    Sort an array using iterative quick sort with custom Stack.

    Uses your custom Stack class to simulate recursion, avoiding
    potential stack overflow on large or pathological inputs.
    O(n log n) average, O(n²) worst time. O(log n) space.

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
    - Not stable: equal elements may be reordered
    - Uses Lomuto partition scheme with last element as pivot
    - Custom Stack (singly linked list based) provides O(1) push/pop
    - Pushes smaller subarray first to keep stack size O(log n)
    - Worst-case O(n²) for already sorted or reverse sorted arrays

    Examples
    --------
    >>> arr = np.array([38, 27, 43, 3, 9, 82, 10])
    >>> quick_sort(arr)
    array([ 3,  9, 10, 27, 38, 43, 82])
    """
    n = arr.shape[0]

    if n <= 1:
        return arr.copy()

    result = arr.copy()
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


def _lomuto_partition(arr: np.ndarray, low: int, high: int, /) -> int:
    """
    Partition array using Lomuto scheme.

    Selects last element as pivot and rearranges array so that
    all elements <= pivot come before it, all elements > pivot come after.

    Parameters
    ----------
    arr : np.ndarray
        Array to partition (modified in-place).
    low : int
        Start index of partition range.
    high : int
        End index of partition range (pivot position).

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
